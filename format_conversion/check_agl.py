'''
    计算文件校验编码，e.g. md5
'''
import os
import hashlib

_FILE_SLIM = 100 * 1024 * 1024  # 大于 100MB 则进行分片


def mmd5(file_name):
    '''
    :param file_name: 待校验的文件
    :return:
    '''
    # calltimes = 0
    hmd5 = hashlib.md5()
    with open(file_name, 'rb') as fp:
        f_size = os.stat(file_name).st_size
        if f_size > _FILE_SLIM:
            while f_size > _FILE_SLIM:
                hmd5.update(fp.read(_FILE_SLIM))
                f_size /= _FILE_SLIM
                # calltimes += 1   # delete
            if 0 < f_size <= _FILE_SLIM:
                hmd5.update(fp.read())
            else:
                hmd5.update(fp.read())

    return hmd5.hexdigest()

'''
    test md5
'''
# if __name__ == '__main__':
    # test_file = 'E:/desktop/fql_on/positive.csv'
    # print(mmd5(test_file))