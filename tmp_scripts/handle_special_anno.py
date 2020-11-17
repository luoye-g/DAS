# coding: gbk
import os
import cv2
import random

from tmp_scripts.scripts_tools import if_intersection
from mysql.sql_op import query_slide_info, query_annos, insert_annotations, insert_anno_special, update_annotations_special
from slide_read_tools.slide_read_factory import srf
from beans.type_c import Rect, Point
from beans.Anno import Annotation
from format_conversion.codes import cc
from format_conversion.xml_tools import read_xml_by_path

anno_dict = {
    '边缘细胞':         'boarder_cell', 
    '表层及角化细胞':   'surface_keratinocytes', 
    '成团腺细胞':       'clumped_gland',
    '化生':             'metaplasia', 
    '基底及萎缩细胞':    'base_atrophy'
}

image_method_dict = {'01': '3DHistech', '02': 'WNLO' , '03': 'SZSQ', '04': 'SZSQ'}
format_dict = {'3DHistech': 'mrxs', 'WNLO': 'svs' , 'SZSQ': 'sdpc'}
zoom_dict = {'01': '20x', '02': '20x' , '03': '40x', '04': '40x'}
group_dict = {'sfy8p':      ['Shengfuyou_8th', 'Yes'], 
              'sfy7p':      ['Shengfuyou_7th', 'Yes'], 
              'sfy5p':      ['Shengfuyou_5th', 'Yes'], 
              'sfy4p':      ['Shengfuyou_4th', 'Yes'], 
              'sfy3p':      ['Shengfuyou_3th', 'Yes'], 
              'sfy2p':      ['Shengfuyou_2th', 'Yes'], 
              'sfy1p':      ['Shengfuyou_1th', 'Yes'], 
              'sfy1n':      ['Shengfuyou_1th', 'No'], 
              'tj3p':       ['Tongji_3th', 'Yes'], 
              'tj4p':       ['Tongji_4th', 'Yes'], 
              'tj5p':       ['Tongji_5th', 'Yes'], 
              'tj6p':       ['Tongji_6th', 'Yes'], 
              'tj7p':       ['Tongji_7th', 'Yes'], 
              'tj8p':       ['Tongji_8th', 'Yes'], 
              'tj9p':       ['Tongji_9th', 'Yes'], 
              'szsqtj7n':   ['Tongji_7th', 'No'], 
              'szsqtj3p':   ['Tongji_3th', 'Yes'], 
              'szsqtj3n':   ['Tongji_3th', 'No'], 
              'szsqtj4p':   ['Tongji_4th', 'Yes'], 
              'szsqtj4n':   ['Tongji_4th', 'No'], 
              'szsqtj5p':   ['Tongji_5th', 'Yes'], 
              'szsqtj5n':   ['Tongji_5th', 'No'], 
              'szsqtj6n':   ['Tongji_6th', 'No'], 
              'szsqtj8n':   ['Tongji_8th', 'No'], 
              'szsqtj9n':   ['Tongji_9th', 'No'], 
              'szsqsfy1':   ['Shengfuyou_1th', 'Yes'], 
              'szsqsfy3p':  ['Shengfuyou_3th', 'Yes'], 
              'szsqsfy4p':  ['Shengfuyou_4th', 'Yes'], 
              'szsqsfy5p21':['Shengfuyou_5th', 'Yes'],
              'oursfy3':    ['Shengfuyou_3th', 'Yes'], 
              'oursfy4':    ['Shengfuyou_4th', 'Yes'], 
              'oursfy5':    ['Shengfuyou_5th', 'Yes'], 
              'hardslide':  ['a', '1']
              }


def merge_anno(sql_annos, spe_annos):
    '''
    merge model2 recon and anno
    :param sql_annos:
    :param spe_annos:
    :return 
    '''
    spe_insert_annos = []
    sql_update_annos = []
    for s in spe_annos:
        max_iou = 0
        del_flag = False
        update_sql_anno = None
        sr = s.cir_rect_class()
        for sql in sql_annos:
            t = sql.cir_rect_class()
            if_inter, iou = if_intersection(sr.x(), sr.y(), sr.w(), sr.h(), 
                                            t.x(), t.y(), t.w(), t.h())
            if if_inter and iou > 0.1:
                if iou > max_iou:
                    max_iou = iou
                    del_flag = True
                    update_sql_anno = sql
                # print(s.cir_rect(), sql.cir_rect(), sql.anno_class(), iou)
        if not del_flag:
            spe_insert_annos.append(s)
        else:
            sql_update_annos.append(update_sql_anno)
    print(len(sql_annos), len(spe_annos), len(spe_insert_annos), len(sql_update_annos))
    return spe_insert_annos, sql_update_annos


tmp_save_path = 'L:/GXB/tmp1'

xml_path = 'L:/业务文档/TotalLabelFiles/originalBackup/萎缩'
anno_items = os.listdir(xml_path)
anno_items = [x for x in anno_items if x.find('.xml') != -1]

read_tools = srf.get_proxy('sdpc')
for anno_item in anno_items:
    annos, _ = read_xml_by_path(os.path.join(xml_path, anno_item))
    print(anno_item, len(anno_item))

    slide_name = anno_item[: anno_item.find('.')]
    slide_infos = query_slide_info(slide_name=slide_name + '%', slide_format='sdpc')
    slide_infos = [x for x in slide_infos if x.slide_path().find('Atrophy') == -1]
    assert len(slide_infos) == 1
    slide_info = slide_infos[0]
    # read_tools.open(os.path.join(slide_info.slide_path(), slide_info.slide_name()))

    filter_annos = list()
    for anno in annos:
        rect = anno.cir_rect_class()
        # img = read_tools.read_region(rect.x(), rect.y(), rect.w(), rect.h())
        # cv2.imwrite(os.path.join(tmp_save_path, slide_info.slide_name()) + anno.cir_rect() + '.jpg', img)
        # break
        if rect.w() < 20 and rect.h() < 20:
            continue
        filter_annos.append(anno)
    # read_tools.close()
    annos = filter_annos

    sql_annos = query_annos(slide_info.sid())
    spe_insert_annos, sql_update_annos = merge_anno(sql_annos, annos)

    c = 'atrophy'
    for sql_update_anno in sql_update_annos:
        # continue
        update_annotations_special(sql_update_anno.aid(), sql_update_anno.is_typical(), sql_update_anno.is_hard(), 
                                   c , cc.class_to_code[c], sql_update_anno.type())

    for spe_insert_anno in spe_insert_annos:
        # continue
        spe_insert_anno.set_anno_class(c)
        spe_insert_anno.set_anno_code(cc.class_to_code[c])
        spe_insert_anno.set_sid(slide_info.sid())
        spe_insert_anno.set_is_hard('No')
        insert_annotations([spe_insert_anno])

    continue
    
    update_sql_annos, filter_sep_annos = merge_anno(sql_annos, special_annos)
    print(len(update_sql_annos), len(filter_sep_annos))
    # continue
    for update_sql_anno in update_sql_annos:
        # print(update_sql_anno[1], update_sql_anno[2])
        iaf = update_sql_anno[1]
        type = 'Rect_Special'
        is_typical = 'No'
        is_hard = 'No'
        if iaf[6].find('typical') == 0:
            is_typical = 'Yes'
        if iaf[5] == 'hardsample':
            is_hard = 'Yes'
            anno_class = 'nplus'
        else:
            anno_class = cc.code_to_class[cc.class_to_code[iaf[5]]]
        anno_code = cc.class_to_code[anno_class]
        aid = update_sql_anno[0].aid()
        # update_annotations_special(aid, is_typical, is_hard, anno_class, anno_code, type)
        insert_anno_special(aid, iaf[4])
    
    for iaf in filter_sep_annos:
        #construct annoatations
        # print(iaf)
        # generate anno
        contours = list()
        contours.append([iaf[0], iaf[1]])
        contours.append([iaf[0] + iaf[2], iaf[1]])
        contours.append([iaf[0] + iaf[2], iaf[1] + iaf[3]])
        contours.append([iaf[0], iaf[1] + iaf[3]])
        
        center_point = Point(iaf[0] + iaf[2] / 2, iaf[1] + iaf[3] / 2)
        cir_rect = Rect(iaf[0], iaf[1], iaf[2], iaf[3])

        type = 'Rect_Special'
        has_contours = 'No'
        is_typical = 'No'
        is_hard = 'No'
        if iaf[6].find('typical') == 0:
            is_typical = 'Yes'
        if iaf[5] == 'hardsample':
            is_hard = 'Yes'
            anno_class = 'nplus'
        else:
            anno_class = cc.code_to_class[cc.class_to_code[iaf[5]]]
        anno_code = cc.class_to_code[anno_class]
        color = 'NULL'
        sid = slide_info[4]
        
        anno = Annotation(center_point, cir_rect, contours, anno_class, 
                            anno_code, type, has_contours, color, is_typical)
        anno.set_sid(sid)
        anno.set_is_hard(is_hard)
        # insert_annotations([anno])