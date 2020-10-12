'''
    自定义异常捕获
'''


class SlideError(Exception):
    def __init__(self, message):
        '''
        :param message: 异常信息
        '''
        self.message = message