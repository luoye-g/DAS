
import xlwt
import xlrd
import os
from mysql.sql_con import MySQLProxy

hard_slide_path = 'E:/desktop/fql_on/hard_slide'

def excel_read1(excel_path):
    '''
    读取切片判断信息
    :param excel_path:
    :return:
    '''
    sql_proxy = MySQLProxy()
    sql_proxy.connect()
    excel = xlrd.open_workbook(excel_path)
    for k, sheet_name in enumerate(excel.sheet_names()):
        if sheet_name != 'tj10 review part':
            continue
        print(sheet_name, type(sheet_name))
        sheet = excel.sheet_by_name(sheet_name)
        data = dict()
        data['slide_format'] = 'srp'
        data['pro_method'] = 'BD'
        data['image_method'] = 'BD'
        data['Medical_history'] = 'null'
        data['is_positive'] = 'Yes'
        data['slide_group'] = 'Tongji_10th'
        for row_index in range(sheet.nrows):
            row_vs = sheet.row(row_index)
            if row_index < 1:
                continue
            # print(row_vs)
            slide_name = row_vs[0].value.strip()
            method = row_vs[1].value.strip()
            if slide_name.find('.srp') == -1:
                slide_name += '.srp'

            remarks = row_vs[5].value.strip()
            sub_class = row_vs[4].value.strip()
            if sub_class.find('(') != -1:
                sub_class = sub_class[: sub_class.find('(')]
            if sub_class.find('（') != -1:
                sub_class = sub_class[: sub_class.find('（')]

            if sub_class != '':
                data['slide_name'] = slide_name
                data['sub_class'] = sub_class
                data['remarks'] = remarks
                data['age'] = -1
                print(data)
                data['Medical_history'] = 'null'
                sql_proxy.insert_into_slide_sub_class(data)

    sql_proxy.close()


def excel_read2(excel_path):
    '''
    临时函数，读取hard_slide.xls，并且插入到数据库
    :param excel_path:
    :return:
    '''
    sql_proxy = MySQLProxy()
    sql_proxy.connect()
    excel = xlrd.open_workbook(excel_path)
    for k, sheet_name in enumerate(excel.sheet_names()):

        print(sheet_name, type(sheet_name))
        sheet = excel.sheet_by_name(sheet_name)
        data = dict()

        for row_index in range(sheet.nrows):
            row_vs = sheet.row(row_index)
            if row_index < 1:
                continue
            # print(row_vs)
            data['slide_name'] = row_vs[3].value
            data['slide_group'] = row_vs[2].value
            data['slide_format'] = row_vs[4].value
            data['pro_method'] = row_vs[0].value
            data['image_method'] = row_vs[1].value
            data['is_positive'] = row_vs[5].value
            data['slide_classify_score'] = -1 if row_vs[6].value == '' else row_vs[6].value
            data['pos_num'] = -1 if row_vs[7].value == '' else row_vs[7].value
            data['recon_num'] = -1 if row_vs[8].value == '' else row_vs[8].value
            data['jppos_22'] = -1 if row_vs[9].value == '' else row_vs[9].value
            data['full_anno'] = row_vs[10].value
            data['sub_class'] = row_vs[11].value
            data['p_10_5Num'] = -1 if row_vs[12].value == '' else row_vs[12].value
            sql_proxy.insert_into_slide_hard(data)
            print(data)

    sql_proxy.close()

def excel_read(excel_path):
    '''
    读取困难切片信息
    :param excel_path:  path of excel path
    :return:
    '''

    excel = xlrd.open_workbook(excel_path)
    for k, sheet_name in enumerate(excel.sheet_names()):
        if sheet_name != 'tongji57us_pos':
            continue
        print(sheet_name, type(sheet_name))
        sheet = excel.sheet_by_name(sheet_name)

        row_ls = list()
        for row_index in range(sheet.nrows):
            row_vs = sheet.row(row_index)
            row_l = list()
            row_l.append(sheet_name)
            for p, row_v in enumerate(row_vs):
                # if p == 6:
                #     continue
                row_v = row_v.value
                if type(row_v) is '<class \'str\'>':
                    row_v = row_v.strip()
                row_l.append(row_v)
                break
            if str(row_vs[0].value).strip() is '':
                continue
            if row_index > 0:
                row_ls.append(row_l)

        excel_write(os.path.join(hard_slide_path, sheet_name + '.xls'), row_ls)


def excel_unified_hard():

    excel_path = 'E:/desktop/fql_on/hard_slide'
    xls = os.listdir(excel_path)
    xls = [x for x in xls if x.find('.xls') != -1]
    data = list()

    xls_head = ['pro_method',
                'image_method',
                'slide_group',
                'slide_name',
                'slide_format',
                'is_positive',
                'slide_classify_score',
                'pos_num',
                'recon_num',
                'jppos/22',
                'full_anno',
                'judge',
                'p>10.5Num']
    group_map = {
        'sfy3':     'Shengfuyou_3th',
        'sfy5':     'Shengfuyou_5th',
        'sfy7':     'Shengfuyou_7th',
        'tongji3':  'Tongji_3th',
        'tongji4':  'Tongji_4th',
        'tongji57us':  'Tongji_5th',
        'tongji6':  'Tongji_6th',
        'tongji7':  'Tongji_7th',
        'tongji8':  'Tongji_8th',
        'tongji9':  'Tongji_9th',
        'xyw':      'XiaoYuWei_1th',
        'xyw2':     'XiaoYuWei_2th'
    }

    wb = xlwt.Workbook()
    s1 = wb.add_sheet('a')
    line_index = 0
    for k, head in enumerate(xls_head):
        s1.write(line_index, k, head)
    line_index += 1

    for xl in xls:
        # print(xl)
        tmp_sheet = xlrd.open_workbook(os.path.join(excel_path, xl)).sheet_by_index(0)
        slide_group = None
        is_positive = None
        pro_method = 'Non-BD'
        image_method = 'SZSQ'
        slide_format = 'sdpc'
        if xl == 'szsq_sfy1.xls':
            slide_group = 'Shengfuyou_1th'
            is_positive = 'Yes'
        elif xl == 'tongji4_611_neg.xls':
            slide_group = 'Tongji_4th'
            is_positive = 'No'
        else:
            us = xl.split('_')
            slide_group = group_map[us[0]]
            is_positive = 'Yes' if us[1] == 'pos.xls' else 'No'

        print(xl, slide_group, is_positive)

        for row in range(1, tmp_sheet.nrows):
            cur_row = tmp_sheet.row(row)
            s1.write(line_index, 0, pro_method)
            s1.write(line_index, 1, image_method)
            s1.write(line_index, 2, slide_group)
            slide_name = None
            v = str(cur_row[1].value)
            if v.find('.sdpc') == -1:
                slide_name = v + '.sdpc'
            else:
                slide_name = v[: v.find('.sdpc')] + '.sdpc'
            s1.write(line_index, 3, slide_name)
            s1.write(line_index, 4, slide_format)
            s1.write(line_index, 5, is_positive)

            for k in range(2, len(cur_row)):
                s1.write(line_index, k + 4, cur_row[k].value)
            line_index += 1
            # print(cur_row)
            # print(tmp_sheet.row(row))
    wb.save('hard_slide_unified.xls')

def excel_write(excel_path, data=None):
    '''
    :param excel_path: 写excel的路径
    :param data:       写数据
    '''

    xls_head = ['slide_group', 'slide_name', 'slide_classify_score', 'pos_num', 'recon_num', 'jppos/22', '全片标注',
                '判断', 'p>10.5Num']
    xls_widt = [256 * 20, 256 * 20, 256 * 20, 256 * 10, 256 * 10, 256 * 10, 256 * 20, 256 * 20, 256 * 20]
    wb = xlwt.Workbook()
    s1 = wb.add_sheet('a')
    line_index = 0
    for k, head in enumerate(xls_head):
        s1.write(line_index, k, head)
        s1.col(k).width = xls_widt[k]
    line_index += 1

    for line in data:
        for k, uint in enumerate(line):
            if k >= len(xls_head):
                break
            s1.write(line_index, k, uint)
        line_index += 1

    # s1.write_merge(1, 1, 1, 3, 'x')

    wb.save(excel_path)


if __name__ == '__main__':

    excel_path = 'hard_slide_unified.xls'
    excel_read2(excel_path)

    # excel_unified_hard()
    # excel_write('L:/GXB/fql_on/text.xls')