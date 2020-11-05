import json
import numpy as np
import datetime

# class JsonEncoder(json.JSONEncoder):

#     def default(self, obj)
#     def default(self, obj):
#         if isinstance(obj, np.integer):
#             return int(obj)
#         elif isinstance(obj, np.floating):
#             return float(obj)
#         elif isinstance(obj, np.ndarray):
#             return obj.tolist()
#         elif isinstance(obj, datetime):
#             return obj.__str__()
#         else:
#             return super(MyEncoder, self).default(obj)

def load_dict(file_name):
    '''
    :param file_name: load dict file name
    return dict
    '''
    with open(file_name, 'r') as file:
        dic = json.load(file)
    return dic


def save_dict(dic, file_name):
    '''
    :param dic:
    :param file_name:
    '''
    