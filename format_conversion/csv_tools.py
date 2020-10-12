from format_conversion.libs._csv_tools import __read_csv_by_path__

def read_csv_by_path(csv_path, csv_name, level=0):
    '''
    :param csv_path: csv file path
    :param csv_name:
    :param level: 读取坐标的层级，默认为0
    :return:
    '''
    return __read_csv_by_path__(csv_path, csv_name, level)