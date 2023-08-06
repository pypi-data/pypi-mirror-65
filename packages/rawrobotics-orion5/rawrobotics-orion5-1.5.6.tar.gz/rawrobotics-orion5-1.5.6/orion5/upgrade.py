"""A one line summary of the module or program, terminated by a period.

Leave one blank line.  The rest of this docstring should contain an
overall description of the module or program.  Optionally, it may also
contain a brief description of exported classes and functions and/or usage
examples.

  Typical usage example:

  foo = ClassFoo()
  bar = foo.FunctionBar()
"""

import math


class Angle(object):
    @staticmethod
    def from_units(value, units):
        func_name = f'from_{units}'
        func = getattr(Angle, func_name, None)

        if func is not None:
            value = float(value)
            return func(value)

        raise ValueError(f"units '{units}' not implemented")

    @classmethod
    def from_radians(cls, value):
        return cls(math.degrees(value))

    @classmethod
    def from_deg180(cls, value):
        return cls(Angle.wrap360(value))

    @classmethod
    def from_deg360(cls, value):
        return cls(Angle.wrap360(value))

    @classmethod
    def from_cytron(cls, value):
        return cls(value * 360.0 / 1088.0)

    def __init__(self, value):
        self.value = self.wrap360(value)

    def to_radians(self):
        return math.radians(self.value)

    def to_deg180(self):
        return self.wrap180(self.value)

    def to_deg360(self):
        return self.value

    def to_cytron(self):
        return int(self.value * 1088.0 / 360.0)

    @staticmethod
    def wrap180(angle):
        angle = (angle + 180.0) % 360.0
        if angle < 0:
            angle += 360.0
        return angle - 180.0

    @staticmethod
    def wrap360(value):
        if value < 0:
            value += 360.0
        elif value >= 360.0:
            value -= 360.0
        return value

    def __repr__(self):
        return f'Angle( {self.value:.2f} deg )'


class Params(dict):
    """Summary of class here.

    Longer class information....
    Longer class information....

    Attributes:
        likes_spam: A boolean indicating if we like SPAM or not.
        eggs: An integer count of the eggs we have laid.
    """

    def __init__(self, params):
        assert isinstance(params, dict), f'params is a {type(params)} it must be a dict'
        for key, value in params.items():
            params[key] = {
                'value': value,
                'changed': False,
                'checker': 0
            }
        super().__init__(params)

    def __getitem__(self, key):
        print('GET', key)
        item = dict.__getitem__(self, key)
        return item['value']

    def __setitem__(self, key, val):
        print('SET', key, val)
        item = dict.__getitem__(self, key)
        item['value'] = val
        item['changed'] = True


class BaseClassWithParams(object):
    def __init__(self, params):
        self._params = Params(params)
        self._init_finished = True

    def __getattr__(self, name):
        if '_params' in self.__dict__:
            if name in self._params:
                return self._params[name]
        return self.__dict__[name]

    def __setattr__(self, name, value):
        if '_params' in self.__dict__ and name in self._params:
            self._params[name] = value

        elif '_init_finished' in self.__dict__:
            raise AttributeError(f"'{type(self).__name__}' object has no attribute '{name}'")

        else:
            super().__setattr__(name, value)


class Orion5(BaseClassWithParams):
    def __init__(self):
        params = {
            'baseOffset':         0,
            'shoulderOffset':     0,
            'elbowOffset':        0,
            'wristOffset':        0,
            'clawOffset':         0,
            'baseDirection':     -1,
            'shoulderDirection': -1,
            'elbowDirection':     1,
            'wristDirection':    -1,
            'clawDirection':      1,
            'clawLoadLimit':    500,
            'fieldInflation':     5,
            'clawHomePos':      362,
            'firmwareUpdate':     0,
            'mode':               0,
            'estop':              0,
            'firmwareVersion':   -1,
            'serialNum':         -1
        }
        super().__init__(params)


class Joint(BaseClassWithParams):
    def __init__(self, index, name, cw_limit, ccw_limit, margin, slope, punch, speed, mode, invert, initial_pos):
        self.index = index
        self.name = name

        params = {
            # settings
            'cwAngleLimit': cw_limit,
            'ccwAngleLimit': ccw_limit,
            'cwMargin': margin,
            'ccwMargin': margin,
            'cwSlope': slope,
            'ccwSlope': slope,
            'punch': punch,
            'inverter': invert,

            # control
            'enable': 0,
            'goalPosition': initial_pos,
            'desiredSpeed': speed,
            'controlMode': mode,

            # feedback
            'currentPosition': None,
            'currentVelocity': None,
            'currentLoad': None,
            'error': None,
            'moving': None,
            'approachDist': None,
            'goalDistance': None,
        }


if __name__ == '__main__':

    x = Angle.from_cytron(0)
    y = Angle.from_cytron(1087)

    print(x)
    print(y)

    print(x.to_radians())
    print(x.to_deg180())
