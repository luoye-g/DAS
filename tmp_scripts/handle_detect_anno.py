import os
import cv2
from format_conversion.xml_tools import read_detection_xml
from mysql.sql_op import query_slide_info, query_annos, insert_anno_detection
from format_conversion.codes import cc
from slide_read_tools.slide_read_factory import srf
from tmp_scripts.scripts_tools import if_intersection

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
        x = anno.cir_rect_class().x()
        y = anno.cir_rect_class().y()
        w = anno.cir_rect_class().w()
        h = anno.cir_rect_class().h()
        img = slide_read.read_region(x, y, w, h)
        sp = sp = os.path.join(tmp_save_path, name + '_' + anno.cir_rect() + '_' +
                             anno.anno_class() + '.jpg')
        cv2.imwrite(sp, img)
    slide_read.close()

def merge_detct_and_sql(xml_annos, sql_annos):
    '''
    :param xml_annos:
    :param sql_annos:
    '''
    slide_read.open(os.path.join(slide_info.slide_path(), slide_info.slide_name()))
    insert_anno_detections = list()
    for xml_anno in xml_annos:
        xml_rect = xml_anno.cir_rect_class()
        max_iou, detection = 0, None
        for sql_anno in sql_annos:
            sql_rect = sql_anno.cir_rect_class()
            if_inter, iou = if_intersection(xml_rect.x(), xml_rect.y(), 
                                            xml_rect.w(), xml_rect.h(), 
                                            sql_rect.x(), sql_rect.y(), 
                                            sql_rect.w(), sql_rect.h())
            if if_inter:
                # print(xml_anno.cir_rect())
                if iou > max_iou:
                    max_iou = iou
                    detection = [sql_anno.aid(), xml_anno.cir_rect()]
                if True:
                    # print(sql_anno.has_contours(), sql_anno.contours_text())
                    minx = min(xml_rect.x(), sql_rect.x())
                    miny = min(xml_rect.y(), sql_rect.y())
                    maxx = max(xml_rect.x() + xml_rect.w(), sql_rect.x() + sql_rect.w())
                    maxy = max(xml_rect.y() + xml_rect.h(), sql_rect.y() + sql_rect.h())
                    img = slide_read.read_region(minx, miny, maxx - minx + 1, maxy - miny + 1).copy()

                    img = cv2.rectangle(img, (xml_rect.x() - minx, xml_rect.y() - miny), 
                                    (xml_rect.x() + xml_rect.w() - minx, xml_rect.y() - miny + xml_rect.h()), 
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
                    sp = os.path.join(tmp_save_path, name + '_' + xml_anno.cir_rect() + '_' +
                                xml_anno.anno_class() + '.jpg')
                    cv2.imwrite(sp, img)
                    print(xml_anno.cir_rect(), sql_anno.cir_rect(), iou, sql_anno.has_contours())
        if detection is not None:
            insert_anno_detections.append(detection)
    slide_read.close()
    print(len(xml_annos), len(insert_anno_detections))
    return insert_anno_detections
# path
tmp_save_path = 'L:/GXB/tmp1'
slide_path = 'H:/TCTDATA'
slide_format = 'sdpc'

detect_path = 'L:/GXB/lixu/label_adjusted'
xml_items = os.listdir(detect_path)
for xml_item in xml_items[2: ]:
    xmls = os.listdir(os.path.join(detect_path, xml_item))
    xmls = [x for x in xmls if x.find('.xml') != -1]
    us = xml_item.split('_')
    pro_method = 'Non-BD'
    image_method = us[0]
    slide_group = us[1] + '_' + us[2]
    is_positive = 'Yes'
    zoom = cc.zoom_dict[image_method]
    slide_format = cc.format_dict[image_method]

    slide_read = srf.get_proxy(slide_format)
    for xk, xml in enumerate(xmls):
        name = xml[: xml.find('.xml')]
        # handle detection xml
        c_xml_path = os.path.join(detect_path, xml_item, xml)
        xml_annos, _ = read_detection_xml(c_xml_path)
        print('(%d/%d)' % (xk + 1, len(xmls)), c_xml_path, len(xml_annos))
        

        # query slide info
        slide_list = query_slide_info(pro_method, image_method, slide_group, is_positive, slide_format, 
                                      name + '.' + slide_format, zoom)
        assert len(slide_list) == 1
        slide_info = slide_list[0]
        # check annos
        # save_tmp_img(slide_read, xml_annos, slide_info, tmp_path)

        sql_annos = query_annos(slide_info.sid())
        print('sql annos len: ', len(sql_annos))
        # check sql annos
        # save_tmp_img(slide_read, sql_annos, slide_info, tmp_save_path)
        
        insert_anno_detections = merge_detct_and_sql(xml_annos, sql_annos)

        for anno_detection in insert_anno_detections:
            pass
            # insert_anno_detection(anno_detection[0], anno_detection[1])
        break
    break