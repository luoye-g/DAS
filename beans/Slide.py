from beans.type_c import *

slide_pps =  {'slide_path':         mstr,
              'slide_name':         mstr,
              'slide_group':        mstr,
              'pro_method':         mstr,
              'image_method':       mstr,
              'mpp':                f,
              'zoom':               mstr,
              'slide_format':       mstr,
              'format_trans':       mstr,
              'is_positive':        mstr,
              'sub_class':          mstr,
              'is_hard':            mstr,
              'width':              f,
              'height':             f,
              'bounds_x':           f,
              'bounds_y':           f,
              'modify_info':        mt,
              'file_permission':    mstr,
              'md5_info':           mstr}
class SlideInfo:

    def __init__(self,
                 slide_path,
                 slide_name,
                 slide_group,
                 pro_method,
                 image_method,
                 mpp,
                 zoom,
                 slide_format,
                 format_trans,
                 is_positive,
                 is_hard,
                 width,
                 height,
                 sub_class=None,
                 bounds_x=0,
                 bounds_y=0,
                 modify_info=None,
                 file_permission=None,
                 md5_info=None):
        '''
        :param slide_path:      切片路径
        :param slide_name:      切片名称
        :param slide_batch:     切片批次
        :param pro_method:      制片方法
        :param image_method:    成像方法
        :param mpp:             分辨率
        :param zoom:               倍率20x或其它
        :param width:           切片宽
        :param height:          切片高
        :param slide_format:    切片格式
        :param format_trans:    是否是其它格式转化
        :param is_positive:     是否是阳性切片
        :param sub_class:       切片子类
        :param is_hard:         是否是困难切片
        :param bounds_x:        切片前景x方向起始坐标
        :param bounds_y:        切片前景y方向起始坐标
        :param modify_info:     修改信息
        :param file_permission:  文件权限
        :param md5_info:        md5信息
        '''
        self.properties = slide_pps
        self._slide_path = slide_path
        self._slide_name = slide_name
        self._slide_group = slide_group
        self._pro_method = pro_method
        self._image_method = image_method
        self._mpp = mpp
        self._zoom = zoom
        self._slide_format = slide_format
        self._format_trans = format_trans
        self._is_positive = is_positive
        self._sub_class = sub_class
        self._is_hard = is_hard
        self._width = width
        self._height = height
        self._bounds_x = bounds_x
        self._bounds_y = bounds_y
        self._modify_info = modify_info
        self._file_permission = file_permission
        self._md5_info = md5_info

    def slide_path(self): return self._slide_path
    def slide_name(self): return self._slide_name
    def slide_group(self): return self._slide_group
    def pro_method(self): return self._pro_method
    def image_method(self): return self._image_method
    def mpp(self): return self._mpp
    def zoom(self): return self._zoom
    def slide_format(self): return self._slide_format
    def format_trans(self): return self._format_trans
    def is_positive(self): return self._is_positive
    def sub_class(self): return self._sub_class
    def is_hard(self): return self._is_hard
    def width(self): return self._width
    def height(self): return self._height
    def bounds_x(self): return self._bounds_x
    def bounds_y(self): return self._bounds_y
    def modify_info(self): return self._modify_info.c_str()
    def file_permission(self): return self._file_permission
    def md5_info(self): return self._md5_info


    @staticmethod
    def map_to_SlideInfo(m):
        '''
        :param m:  各个参数值的map
        :return:
        '''
        return SlideInfo(m['slide_path'], m['slide_name'], m['slide_group'], m['pro_method'],
                         m['image_method'], m['mpp'], m['zoom'], m['slide_format'], m['format_trans'],
                         m['is_positive'], m['is_hard'], m['width'], m['height'], m['sub_class'],
                         m['bounds_x'], m['bounds_y'], m['modify_info'], m['file_permission'],
                         m['md5_info'])