# coding: gbk
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

def read_model2_txt(txt_path, mpp):
    coors = list()
    size = 256 * 0.293 / mpp
    with open(txt_path, 'r') as txts:
        for line in txts:
            line = line.strip()
            us = line.split(',')
            grade = float(us[0])
            if grade <= 0.5:
                continue
            x = int(int(us[1]) - size / 2)
            y = int(int(us[2]) - size / 2)
            w = int(size)
            h = int(size)
            anno_class = 'pos'
            coors.append([x, y, w, h, anno_class])
    return coors

def merge_anno(sql_annos, fps_annos):
    '''
    merge model2 recon and anno
    :param sql_annos:
    :param fps_annos:
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

import json
def read_detection_json(json_path, anno_class = 'nplus'):
    coors = list()
    with open(json_path, 'r', encoding='utf8')as fp:
        json_data = json.load(fp)
        for item in json_data:
            coors.append([item['x'], item['y'], item['w'], item['h'], anno_class])
    return coors



if __name__ == "__main__":
    read_detection_json('L:/GXB/lixu/FP_3000/FP_3000/BD/Xiehe_1th/TG2323474.json')