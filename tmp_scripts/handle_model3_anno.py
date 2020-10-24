# coding: gbk
'''
    handle model3 annos
'''
import os
import numpy as np

from slide_read_tools.slide_read_factory import srf

origin_xml_path = 'O:/TransSrp/SZSQ_originaldata/Model3Labelfiles/xml'
recheck_path = 'H:/model3/CSH数据净化0908/CSH数据净化0908/model3_recheck'

model3_dict = {'典型阳性': 'typical_pos', '非典型阳性': 'atypical_pos', '阴性': 'nplus'}
image_dict = {'01': '3DHistech' , '02': 'WNLO' , '03': 'SZSQ', '04': 'srp'}

group_dict = dict()
recheck_list = list()
# read all recheck annos
for key in model3_dict.keys():
    current_path = os.path.join(recheck_path, key)
    img_names = os.listdir(current_path)
    img_names = [x for x in img_names if x.find('.jpg') != -1]
    for img_name in img_names:
        us = img_name.split('__')
        image_method = us[0].split('_')[-1]
        slide_group = us[1]
        slide_name = us[2]
        anno_class = us[3]
        model3_class = us[4]
        x = int(us[7])
        y = int(us[8])
        w = int(us[9])
        h = int(us[10])
        if slide_group.find('sfy') != -1:
            slide_group = 'Shengfuyou_' + \
            slide_group[slide_group.find('sfy') + 3: slide_group.find('sfy') + 4] + 'th'
        else:
            slide_group = 'Tongji_' + \
            slide_group[slide_group.find('tj') + 2: slide_group.find('tj') + 3] + 'th'
        # if image_method == '03':
        #     print(image_method, slide_group, slide_name, anno_class, model3_class, x, y, w, h)
        
        recheck_list.append(['SZSQ', slide_group, slide_name + '.sdpc', anno_class, model3_class, x, y, w, h])

        if slide_group not in group_dict.keys():
            group_dict[slide_group] = image_method

from mysql.sql_op import query_slide_info, query_annos
import cv2
tmp_save_path = 'L:/GXB/tmp'
slide_path = 'H:/TCTDATA'
slide_format = 'sdpc'
# slide_read = srf.get_proxy(slide_format)
# 处理recheck标注
for k, item in enumerate(recheck_list):
    # current_path = os.path.join(slide_path, item[0], item[1], 'Positvie', item[2] + '.' + slide_format)
    # print(current_path)
    # slide_list = query_slide_info('Non-BD', 'SZSQ', item[1], 'Yes', 'sdpc', item[2] + '.' + slide_format, '40x')
    print(item)
    # assert len(slide_list) == 1
    # print(slide_list[0].slide_path())
    # slide_read.open(os.path.join(slide_list[0].slide_path(), slide_list[0].slide_name()))

    # img = slide_read.read_region(item[5], item[6], item[7], item[8])
    # save_path = os.path.join(tmp_save_path, item[2] + '_' + str(k) + '.jpg')
    # cv2.imwrite(save_path, img)

    # slide_read.close()

def if_intersection(x1, y1, w1, h1,
                    x2, y2, w2, h2):
    x = max(x1, x2)
    y = max(y1, y2)
    w = min(x1 + w1, x2 + w2) - x
    h = min(y1 + h1, y2 + h2) - y
    if w <= 0 or h <= 0:
        return False, 0
    
    # cal IOU
    iou = (w * h) / (w1 * h1 + w2 * h2 - w * h)

    return True, iou

def read_model3_txt(txt_path):
    coors = list()
    with open(txt_path, 'r') as txts:
        for line in txts:
            line = line.strip()
            us = line.split(',')
            x = int(us[0])
            y = int(us[1])
            w = int(us[2])
            h = int(us[3])
            anno_class = us[4].split('_')[0]
            coors.append([x, y, w, h, anno_class])
    return coors

def merge_model3_anno(txts_list, anno_list):
    '''
    merge model3 recon and anno
    :param txts_list:
    :param anno_list:
    :return 
    '''
    new_txts_list = list()
    for txt in txts_list:
        del_flag = False
        for anno in anno_list:
            if if_intersection(txt[0], txt[1], txt[2], txt[3], 
                               anno[0], anno[1], anno[2], anno[3])[0]:
                del_flag = True
        if not del_flag:
            new_txts_list.append(txt)
    print(len(new_txts_list), len(txts_list))
    filter_list = list()
    for txt in new_txts_list:
        if txt[4].find('nplus') == -1:
            filter_list.append([txt[0], txt[1], txt[2], txt[3], 'atypical_pos'])
        else:
            filter_list.append([txt[0], txt[1], txt[2], txt[3], 'nplus'])
    filter_list += anno_list
    return filter_list

def filter_anno_by_recheck(anno_list, slide_info, recheck_list):
    '''
    recheck anno_list
    :param anno_list:   wait for check
    :param slide_info:  
    :param recheck_list:
    '''
    
    for k, _ in enumerate(anno_list):
        for recheck in recheck_list:
            # print(recheck)
            # ['SZSQ', slide_group, slide_name, anno_class, model3_class, x, y, w, h]
            
            if slide_info.pro_method() == recheck[0] and \
               slide_info.slide_group() == recheck[1] and \
               slide_info.slide_name() == recheck[2]:
               anno_list[k][4] = [recheck[4], recheck[3]]
    return anno_list


def merge_model3_and_mysql_anno(annos, sql_annos):
    '''
    merge mysql database anno and xml_annos
    :param annos:
    :param sql_annos:
    '''
    new_annos = list()
    for anno in annos:
        # print(anno)
        del_flag = False
        for k, sql_anno in enumerate(sql_annos):
            if_inter, iou = if_intersection(anno[0], anno[1], anno[2], anno[3], \
            sql_anno.cir_rect_class().x(), \
            sql_anno.cir_rect_class().y(), \
            sql_anno.cir_rect_class().w(), \
            sql_anno.cir_rect_class().h())
            if if_inter and iou > 0.1:
                # print(anno, sql_anno.cir_rect(), sql_anno.anno_class(), sql_anno.has_contours(), iou)
                del_flag = True
                if anno[4].find('typical') == 0:
                    sql_annos[k].set_is_typical('Yes')
        if not del_flag:
            new_annos.append(anno)
    return new_annos, sql_annos

def update_anno_tables(new_annos, sql_annos):
    '''
    :param new_annos:
    :param sql_annos:
    return
    '''
    
    pass
    


from format_conversion.xml_tools import read_xml_by_path
xml_path = 'O:/TransSrp/SZSQ_originaldata/Model3Labelfiles/xml'
xml_items = os.listdir(xml_path)
for k, xml_item in enumerate(xml_items):
    xmls = os.listdir(os.path.join(xml_path, xml_item))
    xmls = [x for x in xmls if x.find('.xml') != -1]
    print(xml_item)
    us = xml_item.split('_')

    im = '3DHistech'
    sf = 'mrxs'
    zoom = '20x'
    slide_group = 'Shengfuyou_1th'
    slide_read = srf.get_proxy(sf)
    # set model3_top path
    model3_top50_path = 'H:/model3/reco_top50/3D_Shengfuyou_1th'
    
    for xml in xmls:
        annos, _ = read_xml_by_path(os.path.join(xml_path, xml_item, xml))
        name = xml[: xml.find('.')]
        slide_list = query_slide_info('Non-BD', im, slide_group, 'Yes', sf, 
                                      name + '.' + sf, zoom)
        assert len(slide_list) == 1
        slide_info = slide_list[0]
        slide_read.open(os.path.join(slide_info.slide_path(), slide_info.slide_name()))
        # print(xml_item, xml, len(annos))

        # handle annos
        anno_list = list()
        for anno in annos:
            x = anno.cir_rect_class().x() + slide_info.bounds_x()
            y = anno.cir_rect_class().y() + slide_info.bounds_y()
            w = anno.cir_rect_class().w()
            h = anno.cir_rect_class().h()
            anno_list.append([x, y, w, h, anno.anno_class()])
            # print(x, y, w, h, anno.anno_class())
            # img = slide_read.read_region(x, y, w, h)
            # sp = sp = os.path.join(tmp_save_path, name + '_' + anno.cir_rect() + '.jpg')
            # cv2.imwrite(sp, img)

        if len(annos) < 100:  # recon by model3
            # read model3 recon xml
            print(xml_item, xml, len(annos))
            # handle model3 txt
            txts_list = list()
            coors = read_model3_txt(os.path.join(model3_top50_path, name + '.txt'))
            for coor in coors:
                x = coor[0] + slide_info.bounds_x() - int(coor[2] / 2)
                y = coor[1] + slide_info.bounds_y() - int(coor[3] / 2)
                w = coor[2]
                h = coor[3]
                txts_list.append([x, y, w, h, coor[4]])
                sp = os.path.join(tmp_save_path, name + '_' + str(coor) + '.jpg')
                # cv2.imwrite(sp, img)
            merged_list = merge_model3_anno(txts_list, anno_list)

        else:  # recon by model2
            # read model2 recon xml
            
            print(xml_item, xml, len(annos))
        
        slide_read.close()


        # Correct the label according to recheck
        annos = filter_anno_by_recheck(merged_list, slide_info, recheck_list)

        # select annos from mysql database
        sql_annos = query_annos(slide_info.sid())
        print(len(sql_annos))

        # merge model3 anno and origin mysql anno
        new_annos, sql_annos = merge_model3_and_mysql_anno(annos, sql_annos)
        # update database
        update_anno_tables(new_annos, sql_annos)
        break

    break