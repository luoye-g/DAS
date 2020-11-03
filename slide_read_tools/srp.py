
# from libs.sdpc.sdpc import Sdpc
from slide_read_tools.libs.srp.pysrp import Srp
import numpy as np

class SrpProxy:

    def __init__(self):
        self._ors = Srp()

    def open(self, slide_path):
        '''
        :param slide_path:
        :return, :
        '''
        self._ors.open(slide_path)
        self._proporties = self._ors.getAttrs()
        # print(self._proporties)

    def read_region(self, x, y, w, h, level=0):
        '''
        :param x: 
        :param y:
        :param w:
        :param h:
        :param level:
        '''
        img = self._ors.ReadRegionRGB(level, x, y, w, h)
        img = np.ctypeslib.as_array(img)
        img.dtype = np.uint8
        img = img.reshape((h, w, 3))
        img = np.uint8(img)
        return img

    def mpp(self): return self._mppx()
    def _mppx(self): return self._proporties['mpp']
    def _mppy(self): return self._proporties['mpp']
    def boundsx(self): return 0
    def boundsy(self): return 0
    def width(self): return self._proporties['width']
    def height(self): return self._proporties['height']

    def close(self):
        if self._ors is not None:
            self._ors.close()


srr = SrpProxy()