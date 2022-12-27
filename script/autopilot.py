import numpy as np

from kinematic import speed_control


class Autopilot:

    _speed_1 = 0
    _speed_2 = 0

    def __init__(self, speed_max, delta_max):
        self._speed_max = speed_max
        self._delta_max = delta_max

    def get_speed(self):
        return self._speed_1, self._speed_2
    def init_speed(self):
        self._speed_1 = self._speed_max
        self._speed_2 = self._speed_max

        return self.get_speed()

    def compute_speed(self, delta):
        speed = self._speed_max
        r = 1
        if delta // self._delta_max == 0 :
            r = (self._delta_max - delta % self._delta_max) / self._delta_max
            speed = self._speed_max * r

        print(r)

        self._speed_1, self._speed_2 = speed, speed

        if delta > 0 :
            self._speed_2 += self._speed_max * r
        else :
            self._speed_1 += self._speed_max * r

        return self.get_speed()

    def test(self, a, b, delta):
        speed = speed_control(a * delta, 1/(np.absolute(delta) + 1) * b)
        return speed
