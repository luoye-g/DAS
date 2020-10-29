import openslide
import numpy as np

class SvsProxy:

    def __init__(self):
        self._ors = None

    def open(self, slide_path):
        '''
        :param slide_path:
        :return, '\\':
        '''
        # print(slide_path)
        self._ors = openslide.OpenSlide(slide_path)
        self._proporties = self._ors.properties
        # print(self._proporties)

    def mpp(self):
        mpp = self._mppx()
        if mpp.find(';') != -1:
            mpp = mpp[: mpp.find(';')]
        return mpp
        
    def _mppx(self): return self._proporties['aperio.MPP']
    def _mppy(self): return self._proporties['aperio.MPP']
    def boundsx(self): 
        try:
            return self._proporties['aperio.Left']
        except:
            return 0
    def boundsy(self): 
        try:
            return self._proporties['aperio.Top']
        except:
            return 0
    def width(self): return self._proporties['openslide.level[0].width']
    def height(self): return self._proporties['openslide.level[0].height']

    def read_region(self, x, y, w, h, level=0):
        img = self._ors.read_region((x, y), level, (w, h))
        img = np.array(img)
        img = img[:, :, 0: 3]
        img = img[:, :, ::-1]
        return img


    def close(self):
        if self._ors is not None:
            self._ors.close()


svr = SvsProxy()