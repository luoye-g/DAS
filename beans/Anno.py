from beans.type_c import *
'''
    标注类，读取xml后每个标注可生成一个Annotation
'''
anno_pp = {'center_point':      pt,
           'cir_rect':          rt,
           'anno_class':        mstr,
           'anno_code':         mstr,
           'type':              mstr,
           'has_contours':      mstr,
           'color':             mstr,
           'is_typical':        mstr
}
class Annotation:
    def __init__(self, center_point, cir_rect, contours, anno_class, anno_code,
                 type='Rect',
                 has_contours='Yes',
                 color=None,
                 is_typical=None):
        '''
        :param center_point:    轮廓中心点
        :param cir_rect:        轮廓外接矩形
        :param contours:        轮廓
        :param anno_class:      标注类别，例如HSIL，LSIL
        :param anno_code:       标注对应的编码
        :param type:            标注轮廓类型，默认为Rect
        :param has_contours:    标注是否有具体的轮廓
        :param color:           标注显示颜色，默认为None
        :param is_typical:      是否典型阳性
        '''
        self._center_point = center_point
        self._cir_rect = cir_rect
        self._contours = contours
        self._anno_class = anno_class
        self._anno_code = anno_code
        self._type = type
        self._has_contours = has_contours
        self._color = color
        self._is_typical = is_typical

    def center_point(self):
        return self._center_point.c_str()

    def cir_rect(self):
        return self._cir_rect.c_str()

    def cir_rect_class(self):
        return self._cir_rect

    def anno_code(self):
        return self._anno_code

    def is_typical(self):
        return self._is_typical

    def anno_class(self):
        return self._anno_class

    def contours(self):
        return self._contours

    def type(self):
        return self._type

    def color(self):
        return self._color

    def has_contours(self):
        return self._has_contours

    @staticmethod
    def map_to_Anno(m):
        '''
        :param m:  各个参数值的map
        :return:
        '''
        return Annotation(m['center_point'], m['cir_rect'], m['contours'], m['anno_class'],
                         m['anno_code'], m['type'], m['has_contours'], m['color'], m['is_typical'])
