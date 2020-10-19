import sys
sys.path.append('../')

from format_conversion.libs._xml_tools import __read_xml_by_path__
from format_conversion.libs._xml_tools import __save_xml_by_annos__
from format_conversion.libs._xml_tools import __read_xml_by_slide__
from format_conversion.libs._xml_tools import __save_xml_slide_anno__
from format_conversion.libs._xml_tools import __read_xml_slide_anno__
from format_conversion.libs._xml_tools import __merge_anno__

from format_conversion.csv_tools import read_csv_by_path

def read_xml_by_path(xml_path):
    '''
    读取xml并返回标注列表
    :param xml_path: 存储的xml路径
    :return: annos(返回的标注列表)， group_list(暂时不使用)
    '''
    return __read_xml_by_path__(xml_path)


def save_xml_by_annos(annos, xml_path):
    '''
    根据annos与path进行xml文件的存储
    :param annos:   标注集合
    :param path:    存储路径
    :return:        返回是否成功
    '''
    return __save_xml_by_annos__(annos, xml_path)

def save_xml_slide_anno(slide_info, annos, xml_path):
    '''
    根据slide_info and annos save xml
    :param slide_info:
    :param annos:
    :param xml_path:
    :return:
    '''
    __save_xml_slide_anno__(slide_info, annos, xml_path)

def read_xml_slide_anno(xml_path):
    '''
    :param xml_path:
    :return:
    '''
    return __read_xml_slide_anno__(xml_path)
'''
    将各种标注文件转化为xml
'''
def csv_to_xml(csv_path, csv_name, xml_path):
    '''

    :param csv_path:
    :param csv_name:
    :param xml_path: 转化后的xml文件存储路径
    :return:
    '''
    annos, _ = read_csv_by_path(csv_path, csv_name)
    save_xml_by_annos(annos, xml_path)

def read_xml_by_slide(xml_path, slide_path, slide_batch, pro_method, image_method, zoom,
                          format_trans=None,
                          is_positive=True,
                          sub_class=None,
                          is_hard=False):
    '''
    根据原始xml文件与切片文件获取slide_info and annos
    :param xml_path:
    :param slide_path:
    :param slide_batch:
    :param pro_method:
    :param image_method:
    :param zoom:
    :param format_trans:
    :param is_positive:
    :param sub_class:
    :param is_hard:
    :return:
    '''
    return __read_xml_by_slide__(xml_path, slide_path, slide_batch, pro_method, image_method, zoom, format_trans,
                                 is_positive, sub_class, is_hard)

def merge_anno(annos1, annos2):
    '''
    合并两个annos代表的xml标注
    :param annos1:
    :param annos2:
    :return:  返回合并完成的结果
    '''
    return __merge_anno__(annos1, annos2)

'''
    函数测试
'''

if __name__ == '__main__':
    slide_path = 'H:/TCTDATA/3DHistech/Shengfuyou_1th/Positive/01.mrxs'
    xml_path = 'H:/TCTDATA/3DHistech/Shengfuyou_1th/Labelfiles/XML/01.xml'
    # annos, _ = read_xml_by_path(xml_path)
    # slide_batch = 'Shengfuyou_1th'
    # pro_method = 'Non-BD'
    # image_method = '3D'
    # x = '20x'
    # slide_info, annos = read_xml_by_slide(xml_path, slide_path, slide_batch, pro_method, image_method, x,
    #                       format_trans=None,
    #                       is_positive='Yes',
    #                       sub_class=None,
    #                       is_hard='No')

    xml_path = 'D:/PSQ/01.xml'
    # save_xml_by_annos(annos, xml_path)
    # save_xml_slide_anno(slide_info, annos, xml_path)
    slide_info, annos, group_list = read_xml_slide_anno(xml_path)
    target_path = 'D:/PSQ/02.xml'
    save_xml_slide_anno(slide_info, annos, target_path)