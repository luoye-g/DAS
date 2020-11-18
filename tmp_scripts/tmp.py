# delete later
# coding: gbk
import os
import xlrd
import shutil
import cv2
from beans.Anno import Annotation
from beans.type_c import Point, Rect
from format_conversion.codes import cc
from tmp_scripts.scripts_tools import if_intersection
from mysql.sql_op import query_slide_info, query_annos, insert_annotations
from slide_read_tools.slide_read_factory import srf
from format_conversion.csv_tools import csv_read_lines


def merge_anno(sql_annos, fps_annos):
    '''
    merge model2 recon and anno
    :param sql_annos:
    :param spe_annos:
    :return 
    '''
    fps_insert_annos = []
    sql_update_annos = []
    for f in fps_annos:
        max_iou = 0
        del_flag = False
        update_sql_anno = None
        for sql in sql_annos:
            t = sql.cir_rect_class()
            if_inter, iou = if_intersection(f[0], f[1], f[2], f[3], 
                                            t.x(), t.y(), t.w(), t.h())
            if if_inter and iou > 0.1:
                if iou > max_iou:
                    max_iou = iou
                    del_flag = True
                    update_sql_anno = sql
                # print(s.cir_rect(), sql.cir_rect(), sql.anno_class(), iou)
        if not del_flag:
            fps_insert_annos.append(f)
        else:
            if max_iou > 0.8:
                print(max_iou, update_sql_anno.anno_class())
            sql_update_annos.append(update_sql_anno)
    print(len(sql_annos), len(fps_annos), len(fps_insert_annos), len(sql_update_annos))
    # return spe_insert_annos, sql_update_annos


tmp_save_path = 'L:/GXB/tmp1'
csv_path = 'L:/BD_AI_Annos_FP_csv/tongji10_BD'
csvs = os.listdir(csv_path)
csvs = [csv[: csv.find('.csv')] for csv in csvs if csv.find('csv') != -1]

read_tools = srf.get_proxy('srp')
for csv in csvs:
    print(csv)
    slide_infos = query_slide_info(pro_method='BD', slide_name=csv + '.srp')
    assert len(slide_infos) == 1
    slide_info = slide_infos[0]
    mpp = slide_info.mpp()
    csv_lines = csv_read_lines(os.path.join(csv_path, csv + '.csv'))
    csv_annos = list()
    for csv_line in csv_lines:
        csv_uints = csv_line.split(',')
        try:
            cx = int(csv_uints[0])
            cy = int(csv_uints[1])
            wh = int(256 * 0.293 / mpp)
            x = cx - int(wh / 2)
            y = cy - int(wh / 2)
            csv_annos.append([x, y, wh, wh])
        except:
            continue

    sql_annos = query_annos(slide_info.sid())
    print(len(sql_annos))
    merge_anno(sql_annos, csv_annos)

    for iaf in csv_annos:
        contours = list()
        contours.append([iaf[0], iaf[1]])
        contours.append([iaf[0] + iaf[2], iaf[1]])
        contours.append([iaf[0] + iaf[2], iaf[1] + iaf[3]])
        contours.append([iaf[0], iaf[1] + iaf[3]])
        
        center_point = Point(iaf[0] + iaf[2] / 2, iaf[1] + iaf[3] / 2)
        cir_rect = Rect(iaf[0], iaf[1], iaf[2], iaf[3])

        type = 'Rect'
        has_contours = 'No'
        is_typical = 'No'
        is_hard = 'Yes'
        anno_class = 'FP_hard'
        anno_code = cc.class_to_code[anno_class]
        color = 'NULL'
        sid = slide_info.sid()
        
        anno = Annotation(center_point, cir_rect, contours, anno_class, 
                            anno_code, type, has_contours, color, is_typical)
        anno.set_sid(sid)
        anno.set_is_hard(is_hard)
        # insert_annotations([anno])

    # sql_annos = query_annos(slide_info.sid())
    # print(len(sql_annos))
    # merge_anno(sql_annos, csv_annos)
    # read_tools.open(os.path.join(slide_info.slide_path(), slide_info.slide_name()))
    # # check anno
    # mpp = slide_info.mpp()
    # for csv_anno in csv_annos[: 2]:
    #     cx, cy = csv_anno[0], csv_anno[1]
    #     wh = int(256 * 0.293 / mpp)
    #     x = cx - int(wh / 2)
    #     y = cy - int(wh / 2)
    #     img = read_tools.read_region(x, y, wh, wh)
    #     save_name = '%s_%d_%d.jpg' % (csv, cx, cy)
    #     cv2.imwrite(os.path.join(tmp_save_path, save_name), img)
    #     break
    # read_tools.close()

    # print(slide_info.mpp())
    