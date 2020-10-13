import ctypes
import os


class SdpcInfo(ctypes.Structure):
    _fields_ = [("mpp", ctypes.c_double),
                ("level", ctypes.c_int32),

                ("width", ctypes.c_int32),
                ("height", ctypes.c_int32),

                ("tileWidth", ctypes.c_int32),
                ("tileHeight", ctypes.c_int32),

                ("L0_nx", ctypes.c_int32),
                ("L0_ny", ctypes.c_int32)
                ]


class Sdpc(object):
    def __init__(self):
        self.__hand = 0
        if os.name == 'posix':
            dll_path = "libSdpcSdk.so"
        elif os.name == 'nt':
            dll_path = 'SdpcSDK.dll'
        else:
            raise TypeError('Not supported system:{}'.format(os.name))
        current_file_path = os.path.abspath(__file__)
        dll_path = os.path.join(os.path.split(current_file_path)[0], dll_path)
        print('dll or so path:', dll_path)
        self.__dll = ctypes.cdll.LoadLibrary(dll_path)
        #self.__dll = ctypes.cdll.LoadLibrary("/home/zm/cpp-workspace/SdpcSdk/Release/libSdpcSdk.so")
        #print(self.__dll)
        self.__dll.openSdpc.argtypes = [ctypes.c_char_p]
        self.__dll.openSdpc.restype = ctypes.c_ulonglong
        self.__dll.closeSdpc.argtypes = [ctypes.c_ulonglong]
        self.__dll.getSdpcInfo.argtypes = [ctypes.c_ulonglong, ctypes.c_void_p]
        self.__dll.getTile.argtypes = [ctypes.c_ulonglong,  #
                                       ctypes.c_int32, ctypes.c_int32, ctypes.c_int32,  #
                                       ctypes.c_int32, ctypes.c_int32,  #
                                       ctypes.c_char_p]

    # getTile(SdpcHandler handler, int z, unsigned int y, unsigned int x, int w, int h, unsigned char * outbuf)

    def say_hello(self):
        print("hello")

    def open(self, path):
        pStr = ctypes.c_char_p()
        pStr.value = bytes(path, 'utf-8')
        self.__hand = self.__dll.openSdpc(pStr)
        pass

    def close(self):
        if self.__hand != 0:
            self.__dll.closeSdpc(self.__hand)
            self.__hand = 0


    def getAttrs(self):
        info = SdpcInfo()
        ret = self.__dll.getSdpcInfo(self.__hand, ctypes.byref(info))
        if ret == 1:
            attrs = {"mpp": info.mpp,  #
                     "level": info.level,  #
                     "width": info.width,  #
                     "height": info.height  #
                    }
            return attrs
        else:
            return {}

    def getTile(self, z, y, x, w, h):
        img = ctypes.create_string_buffer(w * h * 3)
        ret = self.__dll.getTile(self.__hand, z, y, x, w, h, img)
        if ret == 1:
            return img
        else:
            return None

    # def __del__(self):
    #     self.close()


