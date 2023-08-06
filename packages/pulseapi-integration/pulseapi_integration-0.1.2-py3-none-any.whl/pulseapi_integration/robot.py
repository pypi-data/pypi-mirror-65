import sys
import time
import numpy as np

from pulseapi import *
from pulseapi_integration.linalg import *
from pulseapi_integration.utils import position_2_xyzrpw, list_2_position
from pulseapi_integration.decorators import start_thread, standart_position_output

class Singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]

class NewRobotPulse(RobotPulse, metaclass=Singleton):

    REF_FRAME = np.zeros(6)

    def __init__(self, host=None, logger=None):
        super().__init__(host, logger)

    def move_along_axis(
        self,
        axis: str = '',
        distance: float = 0,
        velocity: float = 0
    ):
        """
        Move along introduced axis on the distance

        :param start_position: move from this point
        :param axis: move along this axis, 'x', 'y', 'z', 'roll', 'pitch', 'yaw'
        :param distance: distance to move
        :param velocity: tcp max velocity
        """
        point = self.get_position()['point']
        rotation =  self.get_position()['rotation']

        linear_axises = {
            'x': 'x',
            'y': 'y',
            'z': 'z'
        }

        rotation_axises = {
            'rx': 'roll',
            'ry': 'pitch',
            'rz': 'yaw'
        }

        try:
            if axis in linear_axises:
                xyz_value = point[linear_axises[axis]]
                point.update({linear_axises[axis]: xyz_value + distance})
                print({linear_axises[axis]: xyz_value + distance})
            elif axis in rotation_axises:
                rpw_value = rotation[rotation_axises[axis]]
                rotation.update({rotation_axises[axis]: rpw_value + math.radians(distance)})
        except KeyError as e:
            raise ValueError(f"Undefined unit: {e.args[0]}. Must be 'x', 'y', 'z', 'rx', 'ry', 'rz'")

        XYZ = point.values()
        RPW = rotation.values()

        self.set_position(position(XYZ, RPW), tcp_max_velocity=velocity, motion_type=MT_LINEAR)
        self.await_stop()

    @start_thread
    def stop_by_digital_input(self, number_of_input):
        """
        Freeze the robot if input pin in the HIGH state
        Remember about await_stop() after trajectory along which you try to detect signal
        :param number_of_input: number of input in control box panel
        """
        while True:
            if self.get_digital_input(number_of_input) == 'HIGH':
                self.freeze()
                print('Contact')
                break

    def sensing(
        self,
        axis,
        detect_distance=0.01,
        detect_velocity=0.001,
        retract_distance=0.01,
        retract_velocity=0.3,
        number_of_input=1
    ):
        """
        Stop the robot when digital input in the HIGH state

        :param axis:
        :param detect_distance: detection distance
        :param detect_velocity: velocity while robot detect the object
        :param number_of_input: digital input number
        :param retract_velocity:
        :param retract_distance:
        """
        self.stop_by_digital_input(number_of_input)
        self.move_along_axis(axis, detect_distance, detect_velocity)
        self.await_stop()

        detect_point = self.get_position()

        if detect_distance < 0:
            self.move_along_axis(axis, retract_distance, retract_velocity)
        else:
            self.move_along_axis(axis, -retract_distance, retract_velocity)

        return detect_point

    def set_reference_frame(self, robot_position):
        self.REF_FRAME = position_2_xyzrpw(robot_position)

    @standart_position_output
    def get_reference_frame(self):
        return self.REF_FRAME

    def set_position(self, target_position, **kwargs):
        from_refFrame_2_baseFrame = self.__from_reference_frame_2_baseframe(target_position)
        # Convert to standart form
        from_refFrame_2_baseFrame = list_2_position(from_refFrame_2_baseFrame)
        self._api.set_position(from_refFrame_2_baseFrame, **kwargs)

        return from_refFrame_2_baseFrame

    def __from_reference_frame_2_baseframe(self, target_position):
        target_position = position_2_xyzrpw(target_position)
        return offset(target_position, self.REF_FRAME)

    def run_positions(self, positions, **kwargs):
        positions_relative_ref_frame = [self.__from_reference_frame_2_baseframe(i) for i in positions]
        positions_relative_ref_frame = [list_2_position(i) for i in positions_relative_ref_frame]

        self._api.run_positions(positions_relative_ref_frame, **kwargs)

        return positions_relative_ref_frame

    @standart_position_output
    def get_position(self):
        """
        Return position relative reverence frame. If reverence frame is equal base frame
        return position relative base frame.
        """
        initial_position = position_2_xyzrpw(self._api.get_position())
        get_position_relative_ref_frame = relRef_frame(initial_position, self.REF_FRAME)

        return get_position_relative_ref_frame

    @standart_position_output
    def get_position_rel_base(self):
        return position_2_xyzrpw(self._api.get_position())

    def go_home(
        self,
        speed=10,
        **kwargs
    ):
        """
        Set robot in home position
        """
        self.set_pose(pose([0, -90, 0, -90, -90, 0]),
                      speed=speed,
                      **kwargs)

    def untwist(self):
        import requests
        answer = requests.put(f'http://{self.host}/untwisting/finish')
        print(answer)