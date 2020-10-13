import openslide

class SvsProxy:

    def __init__(self):
        self._ors = None

    def open(self, slide_path):
        '''
        :param slide_path:
        :return, '\\':
        '''
        self._ors = openslide.OpenSlide(slide_path)
        self._proporties = self._ors.properties
        print(self._proporties)

    def mpp(self): return self._mppx()
    def _mppx(self): return self._proporties['aperio.MPP']
    def _mppy(self): return self._proporties['aperio.MPP']
    def boundsx(self): return self._proporties['aperio.Left']
    def boundsy(self): return self._proporties['aperio.Top']
    def width(self): return self._proporties['aperio.OriginalWidth']
    def height(self): return self._proporties['aperio.Originalheight']


    def close(self):
        if self._ors is not None:
            self._ors.close()


svr = SvsProxy()