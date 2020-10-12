import numpy as np
from beans.Anno import Point, Annotation, Rect
from format_conversion.codes import cc

def sort_sp(csv_lines1, csv_lines2):
    '''
    # 取得各种标记类型
    :param csv_lines1:
    :param csv_lines2:
    :return:
    '''
    # t1 = [[y,x] for y,x in zip(csv_lines1, csv_lines2) if "HISL" in x or "Hisl" in x or "HSIL" in x or 'pos' in x]
    # t2 = [[y,x] for y,x in zip(csv_lines1, csv_lines2) if "LISL" in x or "LISI" in x or "Lisl" in x or "LSIL" in x]
    # t3 = [[y,x] for y,x in zip(csv_lines1, csv_lines2) if "ASCUS" in x or "Ascus" in x or "ASC-US" in x]
    # t4 = [[y,x] for y,x in zip(csv_lines1, csv_lines2) if "AGC" in x or "Agc" in x]
    # t5 = [[y,x] for y,x in zip(csv_lines1, csv_lines2) if "NAEC" in x or "nGEC" in x]
    # t6 = [[y,x] for y,x in zip(csv_lines1, csv_lines2) if "HCG" in x]
    # t7 = [[y,x] for y,x in zip(csv_lines1, csv_lines2) if "SSC" in x or 'nplus' in x]
    # t8 = [[y,x] for y,x in zip(csv_lines1, csv_lines2) if "Normal" in x or "normal" in x]
    # csv_lines_new = t8+t7+t6+t5+t4+t3+t2+t1
    # csv_lines1_new = [y for y,x in csv_lines_new]
    # csv_lines2_new = [x for y,x in csv_lines_new]
    csv_lines1_new = csv_lines1
    csv_lines2_new = csv_lines2
    return csv_lines1_new, csv_lines2_new


def __read_csv_by_path__(csv_path, csv_name, level=0):
    path1 = csv_path + '/' + csv_name + '/file1.csv'
    path2 = csv_path + '/' + csv_name + '/file2.csv'

    csv_lines1 = open(path1, 'r').readlines()
    csv_lines2 = open(path2, 'r').readlines()
    csv_lines1, csv_lines2 = sort_sp(csv_lines1, csv_lines2)  # 一个文件中记录类型和中心坐标，另一个文件中记录轮廓坐标

    annos = list()
    for i in range(0, len(csv_lines1)):  # 0 1
        line = csv_lines2[i]
        elems = line.strip().split(',')
        label = elems[0]
        label1 = elems[1]
        label1 = label1.strip().split(' ')
        label1 = label1[0]

        line = csv_lines1[i]
        line = line[1:(len(line) - 2)]
        elems = line.strip().split('Point:')

        if label1.find("Ellipse") != -1:
            n = len(elems)
            points = [0] * (n - 1)
            for j in range(1, n):
                s = elems[j]
                s1 = s.strip().split(',')
                x = int(np.round(float(s1[0]) / (2 ** level)))
                y = int(np.round(float(s1[1]) / (2 ** level)))
                points[j - 1] = [x, y]
            points = np.stack(points)

        elif label1.find("Polygon") != -1 or label1.find("Rectangle") != -1:
            n = len(elems)
            points = [0] * (n - 1)
            for j in range(1, n):
                s = elems[j]
                s1 = s.strip().split(',')
                x = int(np.round(float(s1[0]) / (2 ** level)))
                y = int(np.round(float(s1[1]) / (2 ** level)))
                points[j - 1] = [x, y]
        # if label == "HISL" or label == "Hisl" or label == "HSIL":  # 不同的类型对应不同的颜色
        #     label = "HISL"
        # elif label == "LISL" or label == "LISI" or label == "Lisl" or label == "LSIL":
        #     label = "LISL"
        # elif label == "ASCUS" or label == "Ascus" or label == "ASC-US":
        #     label = "ASCUS"
        # elif label == "AGC" or label == "Agc":
        #     label = "AGC"
        # elif label == "NAEC" or label == "nGEC":
        #     label = "NAEC"
        # elif label == "HCG":
        #     label = "HCG"
        # elif label == "SSC":
        #     label = "SSC"
        # elif label == 'pos':
        #     label = 'POS'
        # elif label == 'nplus':
        #     label = 'nplus'
        # else:
        #     label = "Normal"
        array_contours = np.array(points)
        center_point = Point(np.mean(array_contours[:, 0]), np.mean(array_contours[:, 1]))
        l, r, t, d = np.min(array_contours[:, 0]), np.max(array_contours[:, 0]), \
                            np.min(array_contours[:, 1]), np.max(array_contours[:, 1])
        bounding_rect = Rect(l, t, r - l, d - t)
        anno = Annotation(center_point, bounding_rect, points, label,
                          cc.class_to_code[label],
                          False, None)
        annos.append(anno)

    return annos, None


def __csv_read_lines(path):
    csv_lines = open(path, 'r').readlines()
    lines = list()
    for line in csv_lines:
        line = line.strip()
        lines.append(line)
    return lines