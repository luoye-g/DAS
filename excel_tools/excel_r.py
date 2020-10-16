

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
                    print(row_v.value.strip(), end='\t')
                else:
                    print(row_v.value, end='\t')
            print('')



if __name__ == '__main__':

    excel_path = 'E:/desktop/fql_on/szsqlHardSlides.xlsx'
    excel_read(excel_path)