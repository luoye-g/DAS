# coding: utf-8
from slide_read_tools.libs.sdpc.sdpc import Sdpc
import numpy as np

class SdpcProxy:

    def __init__(self):
        self._ors = Sdpc()

    def open(self, slide_path):
        '''
        :param slide_path:
        :return, :
        '''
        self._ors.open(slide_path)
        self._proporties = self._ors.getAttrs()
        print(self._proporties)
        if len(self._proporties.keys()) == 0:
            self._proporties = {
                'mpp': -1,
                'width': -1,
                'height': -1,
            }

    def mpp(self): return self._mppx()
    def _mppx(self): return self._proporties['mpp']
    def _mppy(self): return self._proporties['mpp']
    def boundsx(self): return 0
    def boundsy(self): return 0
    def width(self): return self._proporties['width']
    def height(self): return self._proporties['height']

    def read_region(self, x, y, w, h, level=0):
        '''
        :param x: 
        :param y:
        :param w:
        :param h:
        :param level:
        '''
        img = self._ors.getTile(level, y, x, w, h)
        assert img != None
        img = np.ctypeslib.as_array(img)
        img.dtype = np.uint8
        img = img.reshape((w, h, 3))
        img = np.array(img)
        return img

    def close(self):
        if self._ors is not None:
            self._ors.close()


sdr = SdpcProxy()