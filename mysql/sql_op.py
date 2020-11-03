# coding: utf-8
'''
    ���� database das �ľ������
'''
from mysql.sql_con import sql_proxy
from beans.Slide import SlideInfo
from beans.Anno import Annotation
from beans.type_c import Point, Rect

def query_sub_class(pro_method,
                    image_method,
                    slide_group,
                    is_positive,
                    slide_name):
    '''
    :param pro_method:
    :param image_method:
    :param slide_group:
    :param is_positive:
    :param slide_name:
    :return:
    '''
    sub_class = None
    sql = '''select sub_class from slide_sub_class
        where 
        pro_method      like '%s' and
        image_method    like '%s' and
        slide_group     like '%s' and
        is_positive     like '%s' and
        slide_name      like '%s'; ''' % \
    (
        pro_method,
        image_method,
        slide_group,
        is_positive,
        slide_name,
    )
    results = sql_proxy.execute_query(sql)
    if len(results) > 0:
        sub_class = results[0][0]
    return sub_class

def query_hard(sid):
    '''
    :param pro_method:
    :param image_method:
    :param slide_group:
    :param is_positive:
    :param slide_name:
    :return:
    '''
    is_hard = 'No'
    sql = '''select * from slide_hard
        where sid = %d; ''' % \
    (
        sid
    )
    results = sql_proxy.execute_query(sql)
    if len(results) > 0:
        is_hard = 'Yes'
    return is_hard

def query_all_annos():
    '''
    查询所有标注
    :return: 返回特定条件下查询标注的id集合
    '''
    sql = 'select * from annotations'

    sql_proxy.connect()
    results = sql_proxy.execute_query(sql)
    sql_proxy.close()
    id_list = list()
    for res in results:
        uints = res[9].split(';')
        if len(uints) <= 5:
            id_list.append(res[0])
    return id_list


def insert_annotations(annos):
    '''
    :params annos: 
    return None
    '''
    sql = '''insert into annotations (sid, center_point, cir_rect, anno_class, \
        anno_code, type, color, is_typical, contours, is_hard, has_contours) values \
            (%s, '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s');'''
    sql_proxy.connect()
    for anno in annos:
        # print(sql % (anno.sid(), anno.center_point(), anno.cir_rect(), 
        # anno.anno_class(), anno.anno_code(), anno.type(), anno.color(), anno.is_typical(), 
        # anno.contours_text(), anno.is_hard(), anno.has_contours()))
        sql_proxy.exceute_update(sql % (anno.sid(), anno.center_point(), anno.cir_rect(), 
        anno.anno_class(), anno.anno_code(), anno.type(), anno.color(), anno.is_typical(), 
        anno.contours_text(), anno.is_hard(), anno.has_contours()))
    sql_proxy.close()


def insert_anno_detection(aid, detection_box):
    '''
    :param aid: 
    :param detection_box:   
    '''
    sql_proxy.connect()
    sql = 'insert into anno_detection (aid, detection_box) values (%s, \'%s\');' % (aid, detection_box)
    sql_proxy.exceute_update(sql)
    sql_proxy.close()


def del_anno_by_aid(aid):
    '''
    :param aid:
    '''
    sql_proxy.connect()
    sql = 'delete from annotations where aid = %s;' % aid
    sql_proxy.exceute_update(sql)
    sql_proxy.close()


def update_annotations_contours(aid, center_point, cir_rect, contours):
    '''
    :param aid:
    :param center_point:
    :param cir_rect:
    :param contours:
    '''
    sql_proxy.connect()
    sql = 'update annotations set center_point=\'%s\', cir_rect=\'%s\', contours=\'%s\' where aid=%s' % \
            (center_point, cir_rect, contours, aid)
    # print(sql)
    sql_proxy.exceute_update(sql)
    sql_proxy.close()

def update_annoatations_sid(aid, sid):
    '''
    :param aid: primary key
    :param sid: reference key
    '''
    sql_proxy.connect()
    sql = 'update annotations set sid = %s where aid = %s' % (sid, aid)
    sql_proxy.exceute_update(sql)
    sql_proxy.close()


def update_annotations_is_typical(aid, sid, is_typical):
    '''
    :param aid:
    :param sid:
    :param is_typical:
    return 
    '''
    sql_proxy.connect()
    sql = 'update annotations set is_typical=\'%s\' where aid=%s and sid=%s;' % (is_typical, aid, sid)
    sql_proxy.exceute_update(sql)
    sql_proxy.close()

def update_annotations(id_list, type, has_contours):
    '''
    更新is_list集合中的type与has_contours字段
    :param type:    轮廓类型字段
    :has_contours:  是否有具体轮廓
    '''
    sql_proxy.connect()
    for id in id_list:
        sql = 'update annotations set type=\'%s\', has_contours=\'%s\' where aid=%s;' % \
                (type, has_contours, id)
        print(sql)
        sql_proxy.exceute_update(sql)
    sql_proxy.close()

def query_annos(sid):
    '''
    查询切片id = sid 的所有标注
    :param sid: 与该标注关联的sid
    :return:
    '''
    sql = '''select * from annotations where sid = %s;''' % sid

    annos = list()
    sql_proxy.connect()
    results = sql_proxy.execute_query(sql)
    sql_proxy.close()
    for res in results:
        center_point = Point.str_to_Point(res[2])
        cir_rect = Rect.str_to_Rect(res[3])
        anno_class = res[4]
        anno_code = res[5]
        type = res[6]
        color = res[7]
        is_typical = res[8]
        contours = list()
        uints = res[9].split(';')
        for uint in uints:
            if uint == '':
                continue
            us = uint.split(',')
            contours.append([float(us[0]), float(us[1])])
        is_hard = res[10]
        has_contours = res[11]
        
        anno = Annotation(center_point, cir_rect, contours, anno_class, anno_code,
                          type, has_contours, color, is_typical)
        anno.set_is_hard(is_hard)
        anno.set_aid(res[0])
        anno.set_sid(res[1])
        annos.append(anno)

    return annos

def query_slide_info(pro_method='%',
                    image_method='%',
                    slide_group='%',
                    is_positive='%',
                    slide_format='%',
                    slide_name='%',
                    zoom='%'):
    '''
    查询切片信息，以Slide_List方式返回
    :param pro_method:      制片方式 e.g. BD
    :param image_method:    成像方式 e.g. 3DHistech
    :param slide_group:     切片批次 e.g. Shengfuyou_1th
    :param is_positive:     是否阳性 e.g. Yes
    :param slide_format:    切片格式 e.g. mrxs
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
    slide_format    like '%s' and
    slide_name      like '%s' and
    zoom            like '%s'; ''' %\
    (
        pro_method,
        image_method,
        slide_group,
        is_positive,
        slide_format,
        slide_name,
        zoom
    )

    slides = sql_proxy.execute_query(sql)
    # print(len(slides))
    for slide in slides:
        slide_path = slide[1]
        slide_name = slide[2]
        slide_group = slide[3]
        pro_method = slide[4]
        image_method = slide[5]
        mpp = slide[6]
        zoom = slide[7]
        slide_format = slide[8]
        format_trans = slide[14]
        is_positive = slide[9]
        is_hard = query_hard(slide[0])
        width = slide[10]
        height = slide[11]
        sub_class = query_sub_class(pro_method, image_method, slide_group, is_positive, slide_name)
        bounds_x = slide[12]
        bounds_y = slide[13]
        modify_info = None
        file_permission = None
        md5_info = None

        slide_info = SlideInfo(slide_path, slide_name, slide_group, pro_method, image_method, mpp,
                               zoom, slide_format, format_trans, is_positive, is_hard, width, height,
                               sub_class, bounds_x, bounds_y, modify_info, file_permission, md5_info)
        slide_info.set_sid(slide[0])
        # slide_info.show_info()
        slides_list.append(slide_info)

    sql_proxy.close()
    return slides_list

if __name__ == '__main__':
    # query_slide_info(slide_group='Shengfuyou_1th', slide_format='mrxs')

    id_list = query_all_annos()
    print(len(id_list))
    update_annotations(id_list, 'Rectangle', 'No')