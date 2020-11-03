import os
import cv2
# from format_conversion.xml_tools import read_detection_xml
from tmp_scripts.scripts_tools import read_detection_json
from mysql.sql_op import query_slide_info, query_annos, insert_anno_detection, update_annotations_contours
from mysql.sql_op import insert_annotations
from format_conversion.codes import cc
from slide_read_tools.slide_read_factory import srf
from tmp_scripts.scripts_tools import if_intersection
from beans.Anno import Annotation
from beans.type_c import Rect, Point
from format_conversion.codes import cc

import numpy as np


def save_tmp_img(slide_read, annos, slide_info, tmp_path):
    '''
    :param slide_read:      slide read tools
    :param annos:           save annos
    :param slide_info:      slide informtation
    :param tmp_path:        save path
    return 
    '''
    slide_read.open(os.path.join(slide_info.slide_path(), slide_info.slide_name()))
    for anno in annos:
        x = anno[0]
        y = anno[1]
        w = anno[2]
        h = anno[3]
        img = slide_read.read_region(x, y, w, h)
        cir_rect = str(x) + ',' + str(y) + ',' + str(w) + ',' + str(h)
        sp = sp = os.path.join(tmp_save_path, name + '_' + cir_rect + '_' +
                             anno[4] + '.jpg')
        cv2.imwrite(sp, img)
    slide_read.close()

def merge_detct_and_sql(xml_annos, sql_annos):
    '''
    :param xml_annos:
    :param sql_annos:
    '''
    slide_read.open(os.path.join(slide_info.slide_path(), slide_info.slide_name()))
    insert_anno_fp = list()
    update_sql_annos = list()
    del_flag = False
    for xml_anno in xml_annos:
        max_iou, update_sql_anno = 0, None
        del_flag = False
        for sql_anno in sql_annos:
            if sql_anno.anno_class() == 'nplus':
                continue
            sql_rect = sql_anno.cir_rect_class()
            if_inter, iou = if_intersection(xml_anno[0], xml_anno[1], 
                                            xml_anno[2], xml_anno[3], 
                                            sql_rect.x(), sql_rect.y(), 
                                            sql_rect.w(), sql_rect.h())
            if if_inter:
                del_flag = True
                # print(xml_anno.cir_rect())
                if iou > max_iou:
                    max_iou = iou
                    update_sql_anno = sql_anno
                if save_img_flag:
                    # print(sql_anno.has_contours(), sql_anno.contours_text())
                    minx = min(xml_anno[0], sql_rect.x())
                    miny = min(xml_anno[1], sql_rect.y())
                    maxx = max(xml_anno[0] + xml_anno[2], sql_rect.x() + sql_rect.w())
                    maxy = max(xml_anno[1] + xml_anno[3], sql_rect.y() + sql_rect.h())
                    img = slide_read.read_region(minx, miny, maxx - minx + 1, maxy - miny + 1).copy()

                    img = cv2.rectangle(img, (xml_anno[0] - minx, xml_anno[1] - miny), 
                                    (xml_anno[0] + xml_anno[2] - minx, xml_anno[1] - miny + xml_anno[3]), 
                                    (255, 0, 0), 1)
                    img = cv2.rectangle(img, (sql_rect.x() - minx, sql_rect.y() - miny), 
                                    (sql_rect.x() + sql_rect.w() - minx, sql_rect.y() - miny + sql_rect.h()), 
                                    (0, 0, 255), 1)
                    contours = sql_anno.contours()
                    contours = np.array(contours)
                    truncate_contours = []
                    for contour in contours:
                        contour[0] -= minx
                        contour[1] -= miny
                        truncate_contours.append([int(contour[0]), int(contour[1])])
                    img = cv2.drawContours(img, np.array([truncate_contours]), -1, (0, 0, 255))
                    cir_rect = str(xml_anno[0]) + ',' + str(xml_anno[1]) + ',' + str(xml_anno[2]) + ',' + str(xml_anno[3])
                    sp = os.path.join(tmp_save_path, name + '_' + cir_rect + '_' +
                                xml_anno[4] + '_' + sql_anno.anno_class() + '.jpg')
                    cv2.imwrite(sp, img)
                    print(xml_anno, sql_anno.cir_rect(), iou, sql_anno.has_contours())
        
        if not del_flag:
            insert_anno_fp.append(xml_anno)

        # update sql_anno
        # if update_sql_anno is not None and len(update_sql_anno.contours()) <= 4:
        #     # print(max_iou)
        #     update_sql_anno.set_center_point(xml_anno.center_point_class())
        #     update_sql_anno.set_cir_rect(xml_anno.cir_rect_class())
        #     update_sql_anno.set_contours(xml_anno.contours())
        #     update_sql_annos.append(update_sql_anno)

    slide_read.close()
    print(len(xml_annos), len(insert_anno_fp), len(update_sql_annos))
    return insert_anno_fp, update_sql_annos
# path
tmp_save_path = 'L:/GXB/tmp1'

detect_path = 'L:/GXB/lixu/FP_3000/FP_3000/BD'
xml_items = os.listdir(detect_path)


update_sql_flag = True
save_img_flag = True
# WNLO's Shengfuyou_3th and Shengfuyou_5th
for xml_item in xml_items:
    xmls = os.listdir(os.path.join(detect_path, xml_item))
    xmls = [x for x in xmls if x.find('.json') != -1]
    pro_method = 'BD'
    image_method = 'BD'
    slide_group = xml_item
    is_positive = '%'
    zoom = '20x'
    slide_format = 'srp'

    slide_read = srf.get_proxy(slide_format)
    for xk, xml in enumerate(xmls):
        name = xml[: xml.find('.json')]
        # handle detection xml
        c_xml_path = os.path.join(detect_path, xml_item, xml)
        json_annos = read_detection_json(c_xml_path)
        # generate anno by json
        
        print('(%d/%d)' % (xk + 1, len(xmls)), c_xml_path, len(json_annos))
        
        # query slide info
        slide_list = query_slide_info(pro_method, image_method, slide_group, is_positive, slide_format, 
                                      name + '.' + slide_format, zoom)
        assert len(slide_list) == 1
        slide_info = slide_list[0]
        # check annos
        # save_tmp_img(slide_read, json_annos, slide_info, tmp_save_path)
        
        sql_annos = query_annos(slide_info.sid())
        print('sql annos len: ', len(sql_annos))
        # check sql annos
        # save_tmp_img(slide_read, sql_annos, slide_info, tmp_save_path)
        
        insert_anno_fps, update_sql_annos = merge_detct_and_sql(json_annos, sql_annos)

        if not update_sql_flag:
            continue

        for iaf in insert_anno_fps:
            break
            print(iaf)
            # generate anno
            contours = list()
            contours.append([iaf[0], iaf[1]])
            contours.append([iaf[0] + iaf[2], iaf[1]])
            contours.append([iaf[0] + iaf[2], iaf[1] + iaf[3]])
            contours.append([iaf[0], iaf[1] + iaf[3]])
            
            center_point = Point(iaf[0] + iaf[2] / 2, iaf[1] + iaf[3] / 2)
            cir_rect = Rect(iaf[0], iaf[1], iaf[2], iaf[3])

            anno_class = iaf[4]
            anno_code = cc.class_to_code[anno_class]
            type = 'Rect'
            has_contours = 'No'
            is_typical = 'No'
            is_hard = 'No'
            color = 'NULL'
            sid = slide_info.sid()
            
            anno = Annotation(center_point, cir_rect, contours, anno_class, 
                                anno_code, type, has_contours, color, is_typical)
            anno.set_sid(sid)
            anno.set_is_hard(is_hard)
            insert_annotations([anno])
            # insert_anno_detection(anno_detection[0], anno_detection[1])
        
        # correct the sql_annos
        # for usa in update_sql_annos:
        #     update_annotations_contours(usa.aid(), usa.center_point(), usa.cir_rect(), usa.contours_text())
        
        # break
    # break