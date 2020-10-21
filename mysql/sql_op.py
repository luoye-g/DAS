# coding: utf-8
'''
    ���� database das �ľ������
'''
from mysql.sql_con import sql_proxy

def query_slide_info(pro_method='%',
                    image_method='%',
                    slide_group='%',
                    is_positive='%',
                    slide_name='%',
                    zoom='%'):
    '''
    查询切片信息，以Slide_List方式返回
    :param pro_method:      制片方式 e.g. BD
    :param image_method:    成像方式 e.g. 3DHistech
    :param slide_group:     切片批次 e.g. Shengfuyou_1th
    :param is_positive:     是否阳性 e.g. Yes
    :param slide_name:      切片名称 e.g. xxxxx.mrxs
    :param zoom:            切片倍率 e.g. 20x
    :return:
    '''
    slides_list = list()
    sql_proxy.connect()

    # generate sql
    sql = '''select * from slides
    where 
    pro_method      like '%s' and
    image_method    like '%s' and
    slide_group     like '%s' and
    is_positive     like '%s' and
    slide_name      like '%s' and
    zoom            like '%s'; ''' %\
    (
        pro_method,
        image_method,
        slide_group,
        is_positive,
        slide_name,
        zoom
    )

    slides = sql_proxy.execute_query(sql)
    print(len(slides))

    sql_proxy.close()
    return slides_list

if __name__ == '__main__':
    query_slide_info(slide_group='Shengfuyou_1th')