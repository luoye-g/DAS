
import xlwt
import xlrd

def excel_read(excel_path):
    '''
    :param excel_path:  path of excel path
    :return:
    '''

    excel = xlrd.open_workbook(excel_path)

    for sheet_name in excel.sheet_names():
        print(sheet_name)
        sheet = excel.sheet_by_name(sheet_name)

        for row_index in range(sheet.nrows):

            row_vs = sheet.row(row_index)
            for row_v in row_vs:
                if type(row_v.value) is '<class \'str\'>':
                    row_v = row_v.value.strip()
                
            


def excel_write(excel_path, data=None):
    '''
    :param excel_path: 写excel的路径
    :param data:       写数据
    '''
    wb = xlwt.Workbook()

    s1 = wb.add_sheet('for test')

    s1.write(0, 1, 'x')
    s1.write(0, 2, 'x')
    s1.write(0, 3, 'x')

    s1.write_merge(1, 1, 1, 3, 'x')

    wb.save(excel_path)


if __name__ == '__main__':

    excel_path = 'L:/GXB/fql_on/szsqlHardSlides.xlsx'
    excel_read(excel_path)

    # excel_write('L:/GXB/fql_on/text.xls')