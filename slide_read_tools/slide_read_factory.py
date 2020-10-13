from slide_read_tools.mrxs import mrr
from slide_read_tools.svs import svr
from slide_read_tools.sdpc import sdr
from slide_read_tools.srp import srr

class SlideReaderFactory:

    def __init__(self):
        self._support_format = {'mrxs': mrr,
                                'svs':  svr,
                                'sdpc': sdr,
                                'srp':  srr,
                                }

    def get_proxy(self, slide_format):
        '''
        :param slide_format: 传入读取切片格式
        :return: 返回切片读取代理
        '''
        assert slide_format in self._support_format.keys()
        return self._support_format[slide_format]


srf = SlideReaderFactory()