class Group(object):
    def __init__(self, color, name, part_of_group):
        '''
        :param color:           颜色
        :param name:            名称
        :param part_of_group:   类别
        '''
        self._color = color
        self._name = name
        self._part_of_group = part_of_group

class Point:

    def __init__(self, x, y):
        self._x = x
        self._y = y

    def x(self,): return self._x

    def y(self,): return self._y

    def c_str(self): return str(self.x()) + ',' + str(self.y())

    @staticmethod
    def str_to_Point(s):
        u = s.split(',')
        return Point(float(u[0]), float(u[1]))


class Rect:

    def __init__(self, x, y, w, h):
        '''
        :param x: 左上角坐标
        :param y:
        :param w: 宽高
        :param h:
        '''
        self._x = x
        self._y = y
        self._w = w
        self._h = h

    def c_str(self): return str(self._x) + ',' + str(self._y) + ',' + str(self._w) + ',' + str(self._h)

    @staticmethod
    def str_to_Rect(s):
        u = s.split(',')
        return Rect(float(u[0]), float(u[1]), float(u[2]), float(u[3]))
    # def __init__(self, left_top, right_bottom):
    #     '''
    #     :param left_top: 左上角
    #     :param right_bottom:  右下角
    #     '''
    #     self._left_top = left_top
    #     self._right_bottom = right_bottom

class ModifyInfo:
    def __init__(self, name='None', time=None):

        self._name = name
        self._time = time

    def name(self): return self._name

    def time(self): return self._time

    def c_str(self): return self.name() + '+' + self.time()

    @staticmethod
    def str_to_ModifyInfo(s):
        u = s.split('+')
        return ModifyInfo(u[0], u[1])


'''
    切片信息
'''


class F:
    def __call__(self, x): 
        if x.find(';') != -1:
            x = x.replace(';', '')
        return float(x)


class Mstr:
    def __call__(self, x): return str(x)


class ModifyType:
    def __call__(self, x): return ModifyInfo.str_to_ModifyInfo(x)


class PointType:
    def __call__(self, x): return Point.str_to_Point(x)


class RectType:
    def __call__(self, x): return Rect.str_to_Rect(x)


f = F()  # str to float
mstr = Mstr()  # other type to str
mt = ModifyType()  # str to ModifyType
pt = PointType()  # str to Point
rt = RectType()  # str to Rect