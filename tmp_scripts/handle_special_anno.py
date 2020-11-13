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

tmp_save_path = 'L:/GXB/tmp1'

anno_path = 'L:/sub_nplus'
anno_items = os.listdir(anno_path)


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
    filter_sep_annos = list()
    update_sql_annos = list()
    for spe in spe_annos:
        del_flag = False
        max_iou = 0
        update_sql_anno = None
        for sql in sql_annos:
            t = sql.cir_rect_class()
            if_inter, iou = if_intersection(spe[0], spe[1], spe[2], spe[3], 
                                            t.x(), t.y(), t.w(), t.h())
            if if_inter and iou > 0.1:
                if iou > max_iou:
                    max_iou = iou
                    update_sql_anno = sql
                del_flag = True
                # print(spe, sql.cir_rect(), sql.anno_class(), iou)
        if not del_flag:
            filter_sep_annos.append(spe)
        else:
            update_sql_annos.append([update_sql_anno, spe, max_iou])
    # print(len(spe_annos), len(sql_annos), len(filter_sep_annos), len(update_sql_annos))

    return update_sql_annos, filter_sep_annos

from jd.json_utils import load_dict, save_dict
# save_dict(p_slides_dict, 'tmp.json')
# assert 1 == 0
p_slides_dict = load_dict('tmp.json')

group_dict = dict()

log_txt = open(os.path.join(tmp_save_path, 'log.txt'), 'w')
for key in p_slides_dict.keys():
    uints = key.split('__')
    tk = '%s__%s__%s' % (uints[0], uints[1], uints[3])
    # if tk not in group_dict.keys():
    #     group_dict[tk] = [key]
    # else:
    #     if len(group_dict[tk]) > 20:
    #         continue
    #     group_dict[tk].append(key)
    # print(key, len(p_slides_dict[key][1]))
    slide_read = srf.get_proxy(p_slides_dict[key][1][0][5])
    slide_info = p_slides_dict[key][0]
    # slide_read.open(os.path.join(slide_info[0], slide_info[1]))

    annos = p_slides_dict[key][1]
    sid = slide_info[4]
    # print(len(sql_annos))
    sql_annos = query_annos(sid)
    special_annos = list()
    for ind, anno in enumerate(annos):
        log_txt.write(os.path.join(slide_info[0], slide_info[1]) + '\n')
        x, y = anno[8], anno[9]
        w = anno[10]
        h = anno[11]
        x, y = x + slide_info[2], y + slide_info[3]
        if anno[-1].find('02__oursfy5') != -1:
            x = x - int(w / 2) + 256
            y = y - int(h / 2) + 256
        elif anno[-1].find('03__szsqtj3p') != -1:
            x = x - int(w / 2) + int(512 * 0.293 / 0.180321 / 2)
            y = y - int(h / 2) + int(512 * 0.293 / 0.180321 / 2)
        elif tk.find('3DHistech') != -1 and (tk.find('Shengfuyou_1th__No') != -1 or tk.find('Shengfuyou_2th__Yes') != -1):
            x, y = x - slide_info[2], y - slide_info[3]
            x = x - int(w / 2) + int(512 * 0.293 / 0.243 / 2)
            y = y - int(h / 2) + int(512 * 0.293 / 0.243 / 2)
        elif tk.find('WNLO__Shengfuyou_3th') !=- 1:
            x = x - int(w / 2) + 256
            y = y - int(h / 2) + 256
        elif tk.find('WNLO__Shengfuyou_4th') != -1:
            if anno[-1].find('256__256') != -1:
                pass
            elif anno[-1].find('oursfy4') != -1:
                x = x - int(w / 2) + 256
                y = y - int(h / 2) + 256
            else:
                pass
        elif slide_info[0].find('XiaoYuWei') != -1:
            x = x + int(512 * 0.293 / 0.17817 / 2) - int(w / 2)
            y = y + int(512 * 0.293 / 0.17817 / 2) - int(h / 2)
        elif slide_info[0].find('Tongji') != -1 and tk.find('No') != -1:
            x = x - int(w / 2)
            y = y - int(h / 2)
        elif tk.find('SZSQ__Shengfuyou_3th') != -1:
            if anno[-1].find('szsqsfy3p') != -1:
                x = x - int(w / 2) + int(512 * 0.293 / 0.180321 / 2)
                y = y - int(h / 2) + int(512 * 0.293 / 0.180321 / 2)
            else:
                pass
        elif tk.find('SZSQ__Shengfuyou') != -1:
            if anno[-1].find('szsqsfy') != -1:
                x = x - int(w / 2) + int(512 * 0.293 / 0.180321 / 2)
                y = y - int(h / 2) + int(512 * 0.293 / 0.180321 / 2)
            elif anno[-1].find('415__415') != -1:
                x = x - int(w / 2)
                y = y - int(h / 2)
            else :
                pass
        elif tk.find('3DHistech__Shengfuyou_1th__Yes') != -1:
            if anno[-1].find('same') != -1 or anno[-1].find('delete') != -1 or \
               anno[-1].find('new') != -1:
                x, y = x - slide_info[2], y - slide_info[3]
                x = x - int(w / 2) + int(512 * 0.293 / 0.243 / 2)
                y = y - int(h / 2) + int(512 * 0.293 / 0.243 / 2)
            else:
                pass
        
        # x, y, w, h
        sp_class = anno[12]
        concrete_class = anno[6]
        model3_class = anno[7]
        special_annos.append([x, y, w, h, sp_class, concrete_class, model3_class])
    #     img = slide_read.read_region(x, y, w, h)
    #     if not os.path.exists(os.path.join(tmp_save_path, tk)):
    #         os.makedirs(os.path.join(tmp_save_path, tk))
    #     cv2.imwrite(os.path.join(tmp_save_path, tk, anno[-1]), img)
    #     break
    # slide_read.close()

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
        insert_annotations([anno])
log_txt.close()