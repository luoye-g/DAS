import openslide

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


    def close(self):
        if self._ors is not None:
            self._ors.close()


mrr = MrxsProxy()