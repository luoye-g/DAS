from xml.dom import minidom
from beans.Anno import Point, Annotation, Rect, anno_pp, Group
from beans.Slide import SlideInfo, ModifyInfo, slide_pps
from format_conversion.codes import cc
import numpy as np
import os
import time
from slide_read_tools.slide_read_factory import srf
from mexception import SlideError
from format_conversion.check_agl import mmd5

def __read_xml_by_path__(xml_path):
    # 建立列表进行数据的临时存储
    with open(xml_path, 'r', encoding='utf-8') as xml_file:
        dom = minidom.parse(xml_file)  # 通过parse获取解析对象
        root = dom.documentElement  # 进行根节点的获取
        annotations = root.getElementsByTagName('Annotation')  # 获取所有Annotation元素节点
        annotation_groups = root.getElementsByTagName('Group')  # 获取所有Group节点

        annos = list()
        for annotation in annotations:
            color = annotation.getAttribute('Color')
            # name = annotation.getAttribute('Name')
            anno_class = annotation.getAttribute('PartOfGroup')  # 对应标注类别
            type = annotation.getAttribute('Type')
            if anno_class not in cc.class_to_code.keys():
                print(xml_path, anno_class)

            contours = list()
            coordinates = annotation.getElementsByTagName('Coordinate')  # 获得每个标注上的坐标节点
            for coordinate in coordinates:
                # order = coordinate.getAttribute('Order')  # 轮廓点次序
                x = float(coordinate.getAttribute('X'))
                y = float(coordinate.getAttribute('Y'))
                contours.append([x, y])

            has_contours = 'Yes'
            if len(contours) <= 4:
                has_contours = 'No'
            array_contours = np.array(contours)
            center_point = Point(np.mean(array_contours[:, 0]), np.mean(array_contours[:, 1]))
            l, r, t, d = np.min(array_contours[:, 0]), np.max(array_contours[:, 0]), \
                         np.min(array_contours[:, 1]), np.max(array_contours[:, 1])
            bounding_rect = Rect(l, t, r - l, d - t)
            anno = Annotation(center_point, bounding_rect, contours, anno_class,
                              cc.class_to_code[anno_class], type, has_contours, color, 'No')
            annos.append(anno)

        group_list = list()
        for annotation_group in annotation_groups:  # 进行group属性的获取
            color = annotation_group.getAttribute('Color')
            name = annotation_group.getAttribute('Name')
            part_of_group = annotation_group.getAttribute('PartOfGroup')
            group_list.append(Group(color, name, part_of_group))

    return annos, group_list


def __save_xml_by_annos__(annos, xml_path):
    doc = minidom.Document()  # 生成文档目录
    root = doc.createElement('ASAP_Annotations')  # 创建一个根节点对象

    node_annots = doc.createElement('Annotations')
    node_groups = doc.createElement('AnnotationGroups')
    for k in range(0, len(annos)):
        anno = annos[k]
        node_managers = doc.createElement('Annotation')
        node_managers.setAttribute('Name', 'Annotation %d' % k)
        node_managers.setAttribute('Type', anno.type())
        node_managers.setAttribute('PartOfGroup', anno.anno_class())
        node_managers.setAttribute('Color', anno.color())
        node_coords = doc.createElement('Coordinates')
        for j in range(0, len(anno.contours())):
            node_name = doc.createElement('Coordinate')
            node_name.setAttribute('Order', str(j))
            node_name.setAttribute('X', str(anno.contours()[j][0]))
            node_name.setAttribute('Y', str(anno.contours()[j][1]))
            node_coords.appendChild(node_name)

        node_managers.appendChild(node_coords)
        node_annots.appendChild(node_managers)

    # 增加尾端信息
    for k in range(len(cc.type_name)):
        node_group = doc.createElement('Group')
        node_group.setAttribute('Name', 'Annotation Group' + str(k))
        node_group.setAttribute('PartOfGroup', cc.type_name[k])
        node_group.setAttribute('Color', cc.color_value[k])
        node_group.appendChild(doc.createElement('Attributes'))
        node_groups.appendChild(node_group)

    root.appendChild(node_annots)
    root.appendChild(node_groups)
    doc.appendChild(root)

    f = open(xml_path, 'w')
    f.write(doc.toprettyxml(indent="\t"))
    f.close()

    return True


def __xml_func(doc, p_node, p_name, obj):
    t_node = doc.createElement('info')
    t_node.setAttribute('k', p_name)
    t_node.setAttribute('v', str(getattr(obj, p_name)()))
    p_node.appendChild(t_node)

def __save_xml_slide_anno__(slide_info, annos, xml_path):
    doc = minidom.Document()  # 生成文档目录
    root = doc.createElement('Slide_Annos')  # 创建一个根节点对象

    # write slide info
    node_slide = doc.createElement('SlideInfo')
    for property in slide_info.properties:
        __xml_func(doc, node_slide, property, slide_info)
    root.appendChild(node_slide)

    # write annotations
    node_annots = doc.createElement('Annotations')
    for k in range(0, len(annos)):
        anno = annos[k]
        node_managers = doc.createElement('Annotation')
        node_managers.setAttribute('Name', 'Annotation %d' % k)

        for property in anno_pp.keys():
            __xml_func(doc, node_managers, property, anno)

        node_coords = doc.createElement('Coordinates')
        for j in range(0, len(anno.contours())):
            node_name = doc.createElement('Coordinate')
            node_name.setAttribute('Order', str(j))
            node_name.setAttribute('X', str(anno.contours()[j][0]))
            node_name.setAttribute('Y', str(anno.contours()[j][1]))
            node_coords.appendChild(node_name)

        node_managers.appendChild(node_coords)
        node_annots.appendChild(node_managers)
    root.appendChild(node_annots)

    # 增加尾端信息
    node_groups = doc.createElement('AnnotationGroups')
    for k in range(len(cc.type_name)):
        node_group = doc.createElement('Group')
        node_group.setAttribute('Name', 'Annotation Group' + str(k))
        node_group.setAttribute('PartOfGroup', cc.type_name[k])
        node_group.setAttribute('Color', cc.color_value[k])
        node_group.appendChild(doc.createElement('Attributes'))
        node_groups.appendChild(node_group)
    root.appendChild(node_groups)

    doc.appendChild(root)

    with open(xml_path, 'w') as f:
        f.write(doc.toprettyxml(indent="\t"))
        f.close()
        return True

    return False


def __read_xml_by_slide__(xml_path, slide_path, slide_batch, pro_method, image_method, zoom,
                          format_trans=None,
                          is_positive=True,
                          sub_class=None,
                          is_hard=False):
    # get slide format
    slide_format = slide_path[slide_path.rfind('.') + 1:]
    slide_proxy = srf.get_proxy(slide_format)

    # construct slide info
    try:
        slide_proxy.open(slide_path)
        seg = '\\'  # 默认路径分割符
        if slide_path.find(seg) == -1:
            seg = '/'
        slide_name = slide_path[slide_path.rfind(seg) + 1:]
        slide_path = slide_path[:slide_path.rfind(seg)]
        slide_path = slide_path.replace('/', '\\')
        mpp = slide_proxy.mpp()

        # modify person's name and last modify time
        m_name = 'csh'
        m_time = time.strftime('"%Y-%m-%d %I:%M:%S"', time.localtime(os.stat(xml_path).st_ctime))
        modify_info = ModifyInfo(m_name, m_time)

        file_permission = None  # Tentatively None
        md5 = mmd5(xml_path)

        slide_info = SlideInfo(slide_path,
                               slide_name,
                               slide_batch,
                               pro_method,
                               image_method,
                               mpp,
                               zoom,
                               slide_format,
                               format_trans,
                               is_positive,
                               is_hard,
                               width=slide_proxy.width(),
                               height=slide_proxy.height(),
                               sub_class=sub_class,
                               bounds_x=slide_proxy.boundsx(),
                               bounds_y=slide_proxy.boundsy(),
                               modify_info=modify_info,
                               file_permission=file_permission,
                               md5_info=md5)
        slide_proxy.close()
    except:
        raise SlideError("slide read error!")

    annos, _ = __read_xml_by_path__(xml_path)
    return slide_info, annos

def __read_xml_slide_anno__(xml_path):
    # 建立列表进行数据的临时存储
    with open(xml_path, 'r', encoding='utf-8') as xml_file:
        dom = minidom.parse(xml_file)
        root = dom.documentElement

        slide_args = dict()
        slide_node = root.getElementsByTagName('SlideInfo')[0]
        info_nodes = slide_node.getElementsByTagName('info')
        for info_node in info_nodes:
            k = info_node.getAttribute('k')
            v = info_node.getAttribute('v')
            slide_args[k] = slide_pps[k](v)
        slide_info = SlideInfo.map_to_SlideInfo(slide_args)

        annotations = root.getElementsByTagName('Annotation')
        annos = list()
        for annotation in annotations:
            anno_args = dict()
            info_nodes = annotation.getElementsByTagName('info')
            for info_node in info_nodes:
                k = info_node.getAttribute('k')
                v = info_node.getAttribute('v')
                anno_args[k] = anno_pp[k](v)
            slide_info = SlideInfo.map_to_SlideInfo(slide_args)
            contours = list()
            coordinates = annotation.getElementsByTagName('Coordinate')  # 获得每个标注上的坐标节点
            for coordinate in coordinates:
                # order = coordinate.getAttribute('Order')  # 轮廓点次序
                x = float(coordinate.getAttribute('X'))
                y = float(coordinate.getAttribute('Y'))
                contours.append([x, y])
            anno_args['contours'] = contours
            anno = Annotation.map_to_Anno(anno_args)
            annos.append(anno)

        annotation_groups = root.getElementsByTagName('Group')
        group_list = list()
        for annotation_group in annotation_groups:  # 进行group属性的获取
            color = annotation_group.getAttribute('Color')
            name = annotation_group.getAttribute('Name')
            part_of_group = annotation_group.getAttribute('PartOfGroup')
            group_list.append(Group(color, name, part_of_group))

    return slide_info, annos, group_list


def __merge_anno__(annos1, annos2):
    '''
    '''

if __name__ == '__main__':
    xml_path = 'H:/TCTDATA/3DHistech/Shengfuyou_1th/Labelfiles/XML/01.xml'
    slide_path = 'H:/TCTDATA/3DHistech/Shengfuyou_1th/Positive/01.mrxs'

    xml_path = 'E:/desktop/fql_on/unified_xml/3D/Shengfuyou_2th/Positive/69_L.xml'
    # pro_method = 'Non_BD'
    # image_method = '3DHistech'
    # zoom = '20x'
    # format_trans = None
    # is_positive = 'Yes'
    # sub_class = None
    # is_hard = False``
    slide_info, annos, _ = __read_xml_slide_anno__(xml_path)


    xml_path = 'D:/PSQ/69_L.xml'
    __save_xml_slide_anno__(slide_info, annos, xml_path)
