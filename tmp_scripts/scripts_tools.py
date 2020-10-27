

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