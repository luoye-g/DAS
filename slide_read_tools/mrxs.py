import openslide
import numpy as np

class MrxsProxy:

    def __init__(self):
        self._ors = None

    def open(self, slide_path):
        '''
        :param slide_path:
        :return, '\\':
        '''
        self._ors = openslide.OpenSlide(slide_path)
        self._proporties = self._ors.properties
        # print(self._proporties)

    def mpp(self): return self._mppx()
    def _mppx(self): return self._proporties['openslide.mpp-x']
    def _mppy(self): return self._proporties['openslide.mpp-y']
    def boundsx(self): return self._proporties['openslide.bounds-x']
    def boundsy(self): return self._proporties['openslide.bounds-y']
    def width(self): return self._proporties['openslide.bounds-width']
    def height(self): return self._proporties['openslide.bounds-height']

    def read_region(self, x, y, w, h, level=0):
        img = self._ors.read_region((x, y), level, (w, h))
        img = np.array(img)
        img = img[:, :, 0: 3]
        img = img[:, :, ::-1]
        return img

    def close(self):
        if self._ors is not None:
            self._ors.close()


mrr = MrxsProxy()