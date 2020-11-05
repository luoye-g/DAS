# coding: gbk
import os
import cv2
from mysql.sql_op import query_slide_info
from slide_read_tools.slide_read_factory import srf

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
p_slides_dict = {}
imgs_dict = dict()
for anno_item in anno_items:
    
    print(anno_item, anno_dict[anno_item])
    a_class = anno_dict[anno_item]
    groups = os.listdir(os.path.join(anno_path, anno_item))
    for group in groups:
        if not os.path.isdir(os.path.join(anno_path, anno_item, group)):
            continue
        imgs = os.listdir(os.path.join(anno_path, anno_item, group))
        imgs = [img for img in imgs if img.find('.jpg') != -1]
        
        for img in imgs:
            us = img.split('__')
            image_method = image_method_dict[us[0]]
            zoom = zoom_dict[us[0]]
            slide_group = group_dict[us[1]][0]
            is_positive = group_dict[us[1]][1]
            if us[1] == 'hardslide':
                slide_group = '%'
                is_positive = '%'
            name = us[2]
            anno_class = us[3]
            model3_class = us[4]
            x = int(us[7])
            y = int(us[8])
            w = int(us[9])
            h = int(us[10])

            combine_anno_info = [image_method, slide_group, is_positive, zoom, name, format_dict[image_method], 
                                anno_class, model3_class, x, y, w, h, a_class, img]

            # combine key
            key = '%s__%s__%s__%s__%s' % (image_method, slide_group, name, is_positive, zoom)
            if key not in imgs_dict.keys():
                imgs_dict[key] = [combine_anno_info]
            else:
                imgs_dict[key].append(combine_anno_info)
        
        print(len(imgs_dict.keys()))
for key in imgs_dict.keys():
    image_method = imgs_dict[key][0][0]
    slide_group = imgs_dict[key][0][1]
    is_positive = imgs_dict[key][0][2]
    zoom = imgs_dict[key][0][3]
    name = imgs_dict[key][0][4]
    ft = imgs_dict[key][0][5]
    slide_infos = query_slide_info(pro_method='Non-BD', image_method=image_method, zoom=zoom, 
                                    slide_group=slide_group, slide_name=name + '%' + ft, is_positive=is_positive)
    if len(slide_infos) == 0:
        name = name.replace('-', ' ')
        slide_infos = query_slide_info(pro_method='Non-BD', image_method=image_method, zoom=zoom, 
                                        slide_group=slide_group, slide_name=name + '%' + ft, is_positive=is_positive)
        if len(slide_infos) == 0:
            slide_infos = query_slide_info(pro_method='Non-BD', image_method=image_method, zoom=zoom, 
                                        slide_group=slide_group, slide_name='sfy' + name + '%' + ft, is_positive=is_positive)
    if len(slide_infos) > 1:
        slide_infos = query_slide_info(pro_method='Non-BD', image_method=image_method, zoom=zoom, 
                                        slide_group=slide_group, slide_name=name + '.' + ft, is_positive=is_positive)
    if len(slide_infos) == 0:
        slide_infos = query_slide_info(pro_method='Non-BD', image_method=image_method, zoom=zoom, 
                                    slide_group=slide_group, slide_name=name + '%', is_positive=is_positive)
            
    if len(slide_infos) != 1:
        new_slide_infos = list()
        for slide in slide_infos:
            if slide.slide_group().find('th') != -1:
                new_slide_infos.append(slide)
        slide_infos = new_slide_infos
    if len(slide_infos) == 1:
        p_slides_dict[key] = [slide_infos[0], imgs_dict[key]]
    else:
        print(key)
        print(imgs_dict[key])

log_txt = open(os.path.join(tmp_save_path, 'log.txt'), 'w')
for key in p_slides_dict.keys():
    
    print(key, len(p_slides_dict[key][1]))
    slide_read = srf.get_proxy(p_slides_dict[key][1][0][5])
    slide_info = p_slides_dict[key][0]
    slide_read.open(os.path.join(slide_info.slide_path(), slide_info.slide_name()))
    for anno in p_slides_dict[key][1]:
        log_txt.write(os.path.join(slide_info.slide_path(), slide_info.slide_name()) + '\n')
        x = anno[8] + slide_info.bounds_x()
        y = anno[9] + slide_info.bounds_y()
        w = anno[10]
        h = anno[11]
        if slide_info.slide_group().find('Shengfuyou_8th') != -1 or \
           slide_info.slide_group().find('Shengfuyou_7th') != -1:
            x = x - int(w / 2)
            y = y - int(h / 2)
        img = slide_read.read_region(x, y, w, h)
        cv2.imwrite(os.path.join(tmp_save_path, anno[-1]), img)
        break
    slide_read.close()

log_txt.close()