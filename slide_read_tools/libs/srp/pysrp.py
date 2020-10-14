import ctypes
import os
import numpy as np
from PIL import Image

#apt install libsqlite3-dev
#apt install libopencv-dev


class Srp(object):
    def __init__(self):
        self.__hand = 0
        if os.name == 'posix':
            dll_path = "libSrpPython.so"
        elif os.name == 'nt':
            dll_path = 'srp.dll'
        else:
            raise TypeError('Not supported system:{}'.format(os.name))
        current_file_path = os.path.abspath(__file__)
        os.environ["PATH"] += os.pathsep + os.path.split(current_file_path)[0]
        dll_path = os.path.join(os.path.split(current_file_path)[0], dll_path)
        print(dll_path)
        self.__dll = ctypes.cdll.LoadLibrary(dll_path)
        self.__dll.Open.argtypes = [ctypes.c_char_p]
        self.__dll.Open.restype = ctypes.c_ulonglong
        self.__dll.Close.argtypes = [ctypes.c_ulonglong]
        self.__dll.ReadRegionRGB.argtypes = [ctypes.c_ulonglong,  #
                                       ctypes.c_int32, ctypes.c_int32, ctypes.c_int32,  #
                                       ctypes.c_int32, ctypes.c_int32,  #
                                       ctypes.c_char_p, ctypes.POINTER(ctypes.c_int32)]
        self.__dll.ReadParamInt32.argtypes = [ctypes.c_ulonglong, ctypes.c_char_p, ctypes.POINTER(ctypes.c_int32)]
        self.__dll.ReadParamInt64.argtypes = [ctypes.c_ulonglong, ctypes.c_char_p, ctypes.POINTER(ctypes.c_int64)]
        self.__dll.ReadParamFloat.argtypes = [ctypes.c_ulonglong, ctypes.c_char_p, ctypes.POINTER(ctypes.c_float)]
        self.__dll.ReadParamDouble.argtypes = [ctypes.c_ulonglong, ctypes.c_char_p, ctypes.POINTER(ctypes.c_double)]
        self.__dll.WriteParamDouble.argtypes = [ctypes.c_ulonglong, ctypes.c_char_p, ctypes.c_double]
        self.__dll.WriteAnno.argtypes = [ctypes.c_ulonglong, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_double]
        self.__dll.CleanAnno.argtypes = [ctypes.c_ulonglong]
        # self.__dll.CleanManualAnno.argtypes = [ctypes.c_ulonglong]
        self.__dll.WriteManualAnno.argtypes = [ctypes.c_ulonglong, ctypes.c_char_p, ctypes.c_int, #
                                               ctypes.c_double, ctypes.c_double, ctypes.c_double, ctypes.c_double,#
                                               ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char_p]
        self.__dll.ReadManualAnnoCount.argtypes = [ctypes.c_ulonglong, ctypes.POINTER(ctypes.c_int32)]
        self.__dll.ReadManualAnno.argtypes = [ctypes.c_ulonglong, ctypes.c_int, #ctx,n
                                              ctypes.c_char_p, ctypes.POINTER(ctypes.c_int32), #id
                                              ctypes.POINTER(ctypes.c_int32), #type
                                              ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_double),#xywh
                                              ctypes.c_char_p, ctypes.POINTER(ctypes.c_int32),#name
                                              ctypes.c_char_p, ctypes.POINTER(ctypes.c_int32),#text
                                              ctypes.c_char_p, ctypes.POINTER(ctypes.c_int32),#attr
                                              ctypes.c_char_p, ctypes.POINTER(ctypes.c_int32)#style
                                              ]

    def say_hello(self):
        self.__dll.hello()

    def open(self, path):
        print(path)
        pStr = ctypes.c_char_p()
        pStr.value = bytes(path, 'utf-8')
        self.__hand = self.__dll.Open(pStr)
        pass

    def close(self):
        if self.__hand != 0:
            self.__dll.Close(self.__hand)
            self.__hand = 0

    def getAttrs(self):
        pwKey = ctypes.c_char_p()
        pwKey.value = bytes("width", 'utf-8')
        pw = ctypes.c_int32(0)
        b0 = self.__dll.ReadParamInt32(self.__hand, pwKey, ctypes.byref(pw))
        phKey = ctypes.c_char_p()
        phKey.value = bytes("height", 'utf-8')
        ph = ctypes.c_int32(0)
        b1 = self.__dll.ReadParamInt32(self.__hand, phKey, ctypes.byref(ph))
        pzKey = ctypes.c_char_p()
        pzKey.value = bytes("level", 'utf-8')
        plevel = ctypes.c_int32(0)
        b2 = self.__dll.ReadParamInt32(self.__hand, pzKey, ctypes.byref(plevel))
        ppKey = ctypes.c_char_p()
        ppKey.value = bytes("mpp", 'utf-8')
        pmpp = ctypes.c_double(0)
        b3 = self.__dll.ReadParamDouble(self.__hand, ppKey, ctypes.byref(pmpp))
        if b0 and b1 and b2 and b3:
            attrs = {"mpp": pmpp.value,  #
                     "level": plevel.value,  #
                     "width": pw.value,  #
                     "height": ph.value  #
                    }
            return attrs
        else:
            return {}

    def ReadRegionRGB(self, level, x, y, width, height):
        buf_len = width*height*3
        plen = ctypes.c_int32(buf_len)
        img = ctypes.create_string_buffer(buf_len)
        ret = self.__dll.ReadRegionRGB(self.__hand, level, x, y, width, height, img, ctypes.byref(plen))
        if ret > 0:
            return img
        else:
            return img

    def read_region_uint8(self , level , x , y , width , height):
        buf_len = width*height*3
        plen = ctypes.c_int32(buf_len)
        img = ctypes.create_string_buffer(buf_len)
        ret = self.__dll.ReadRegionRGB(self.__hand, level, x, y, width, height, img, ctypes.byref(plen))
        # if ret > 0:
        nimg = np.ctypeslib.as_array(img)
        nimg.dtype = np.uint8
        nimg = nimg.reshape((height, width, 3))
        img = Image.fromarray(np.uint8(nimg))
        return np.uint8(img)
        # else:
        #     return None

    def WriteScore(self, score):
        keyStr = ctypes.c_char_p()
        keyStr.value = bytes("score", 'utf-8')
        return self.__dll.WriteParamDouble(self.__hand, keyStr, score)

    def ReadScore(self , n = 0):
        keyStr = ctypes.c_char_p()
        keyStr.value = bytes("score", 'utf-8')
        pscore = ctypes.c_double(0)
        self.__dll.ReadParamDouble(self.__hand, keyStr, ctypes.byref(pscore) , n , 10)
        return pscore.value

    def WriteAnno(self, x, y, score):
        return self.__dll.WriteAnno(self.__hand, x, y, 0, score)

    def CleanAnno(self):
        return self.__dll.CleanAnno(self.__hand)

    def WriteManualAnnoRect(self, id_char, x, y, width, height):
        idStr = ctypes.c_char_p()
        idStr.value = bytes(id_char, 'utf-8')
        nameStr = ctypes.c_char_p()
        nameStr.value = bytes("rect", 'utf-8')
        textBase64Str = ctypes.c_char_p()
        textBase64Str.value = bytes("PGRpdj5BSeWGmeWFpTwvZGl2Pg==", 'utf-8')
        rect_attr = "x="+str(x)+";y="+str(y)+";width="+str(width)+";height="+str(height)+";bc=rgb(255, 0, 255);bw=6"
        attrStr = ctypes.c_char_p()
        attrStr.value = bytes(rect_attr, 'utf-8')
        rect_style = "stroke=rgb(255, 0, 255);stroke-width=10px;fill-opacity=0"
        styleStr = ctypes.c_char_p()
        styleStr.value = bytes(rect_style, 'utf-8')
        return self.__dll.WriteManualAnno(self.__hand, idStr, 9000, x, y, width, height, nameStr, textBase64Str, attrStr, styleStr)

    def CleanManualAnno(self):
        return self.__dll.CleanManualAnno(self.__hand)


    def __read_manual_anno_count(self):
        num = ctypes.c_int32(0)
        if self.__dll.ReadManualAnnoCount(self.__hand, num):
            return num.value
        else:
            return 0


    def __read_manual_anno(self, n):
        id_str_len = ctypes.c_int32(1024)
        id_str = ctypes.create_string_buffer(1024)

        atype = ctypes.c_int32(0)
        ax = ctypes.c_double(0)
        ay = ctypes.c_double(0)
        aw = ctypes.c_double(0)
        ah = ctypes.c_double(0)

        name_str_len = ctypes.c_int32(128)
        name_str = ctypes.create_string_buffer(128)

        txt_str_len = ctypes.c_int32(65536)
        txt_str = ctypes.create_string_buffer(65536)

        attr_str_len = ctypes.c_int32(512*1024)
        attr_str = ctypes.create_string_buffer(512*1024)

        style_str_len = ctypes.c_int32(512 * 1024)
        style_str = ctypes.create_string_buffer(512 * 1024)

        flag = self.__dll.ReadManualAnno(self.__hand, n,  # ctx,n
                                         id_str, ctypes.byref(id_str_len),  # id
                                         ctypes.byref(atype),  # type
                                         ctypes.byref(ax), ctypes.byref(ay),ctypes.byref(aw),ctypes.byref(ah),#xywh
                                         name_str, ctypes.byref(name_str_len),  # name
                                         txt_str, ctypes.byref(txt_str_len),  # text
                                         attr_str, ctypes.byref(attr_str_len),  # attr
                                         style_str, ctypes.byref(style_str_len))  # style

        if flag:
            ret = {
                "id": id_str.value[:id_str_len.value].decode('ascii').strip(),  #
                "type": atype.value,  #
                "x": ax.value, "y": ay.value,  "w": aw.value, "h": ah.value,  #
                "name": name_str.value[:name_str_len.value].decode('ascii').strip(), #
                "text": txt_str.value[:txt_str_len.value].decode('ascii').strip(),  #
                "attr": attr_str.value[:attr_str_len.value].decode('ascii').strip(),  #
                "style": style_str.value[:style_str_len.value].decode('ascii').strip()#
            }
            return ret

        else:
            return None


    def ReadManualAnno(self):
        annos = []
        num = self.__read_manual_anno_count()
        for n in range(0, num):
            anno = self.__read_manual_anno(n)
            annos.append(anno)
        return annos
