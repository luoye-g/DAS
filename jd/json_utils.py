import json
import numpy as np
import datetime


class JsonEncoder(json.JSONEncoder):

    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        elif isinstance(obj, np.floating):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        elif isinstance(obj, type(datetime)):
            return obj.__str__()
        else:
            return super(JsonEncoder, self).default(obj)

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
    save dict into json file
    :param dic:
    :param file_name:
    '''
    with open(file_name, 'w') as json_file:
        json.dump(dic, json_file, ensure_ascii=False, cls=JsonEncoder)


'''
test Json
'''
if __name__ == '__main__':
    
    pd = {"sd": 1, "sdc": "sd"}
    save_dict(pd, 'tmp.json')

    dic = load_dict('tmp.json')
    for key in dic.keys():
        print(key, dic[key])