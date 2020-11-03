# coding: gbk
import os

from mysql.sql_op import query_slide_info

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
            if us[1] == 'hardslide':
                continue
            slide_group = group_dict[us[1]][0]
            is_positive = group_dict[us[1]][1]
            name = us[2]
            anno_class = us[3]
            model3_class = us[4]
            x = int(us[7])
            y = int(us[8])
            w = int(us[9])
            h = int(us[10])
            # print(us)
            slide_infos = query_slide_info(pro_method='Non-BD', image_method=image_method, zoom=zoom, 
                                           slide_group=slide_group, slide_name=name + '%', is_positive=is_positive)
            if len(slide_infos) == 0:
                name = us[2].replace('-', ' ')
                slide_infos = query_slide_info(pro_method='Non-BD', image_method=image_method, zoom=zoom, 
                                               slide_group=slide_group, slide_name='%' + name + '%', is_positive=is_positive)
            assert len(slide_infos) > 0
            if len(slide_infos) > 1:
                print(us, len(slide_infos))


