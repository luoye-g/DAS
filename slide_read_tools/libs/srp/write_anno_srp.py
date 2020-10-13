import os
import cv2
import numpy as np
from tqdm import tqdm

import sys
from PIL import Image
# from srp_rw import pysrp
# from utils.WsiReader import WReader

class args:

    path = 'H:/model3/wsi/3rd_try_v1'
    target_res = 0.1803
    bs = 1500
    bs_r = int(bs / 2)

    m3_bs = 256 * 0.293 / target_res
    m3_bs_r = int(m3_bs / 2)

    wsi_cl = 'sdpc'

    wsi_path = '/mnt/160_h/model3/srp_data'

    anno_nums = 50
    
    top50_path = 'H:/model3/reco_top50'

if __name__ == "__main__":
    
    # srp = pysrp.Srp()

    batch_names = os.listdir(args.path)
    batch_names = [x for x in batch_names if os.path.isdir(args.path + '/' + x)]

    for i , batch_name in enumerate(batch_names):
        
        if batch_name != 'tj7':
            continue

        txt_names = os.listdir('%s/%s' % (args.path , batch_name))
        txt_names = [x[ : x.find('.txt')] for x in txt_names if x.find('.txt') != -1]


        for j , txt_name in enumerate(txt_names):
            print('%s/%s/positive/%s.srp' % (args.wsi_path , batch_name , txt_name))
            # srp.open('%s/%s/positive/%s.srp' % (args.wsi_path , batch_name , txt_name))
            # print(srp.getAttrs())
            top50_file = open('%s/%s/positive/%s.txt' % (args.top50_path , batch_name , txt_name) , 'w')
            lines = list()
            with open('%s/%s/%s.txt' % (args.path , batch_name , txt_name) , 'r') as tmp:
                for line in tmp:
                    line = line.strip()
                    lines.append(line)
            tps , ntps , nplus = list() , list() , list()
            final_list = list()
            for line in lines:
                uints = line.split(',')
                model2_grade = float(uints[0])
                x = int(uints[1])
                y = int(uints[2])
                model3_grade = float(uints[3]) , float(uints[4]) , float(uints[5])
                
                max_ind = model3_grade.index(max(model3_grade))
                if max_ind == 0:
                    tps.append([x , y , model3_grade[0] , 'typical_pos'])
                if max_ind == 1:
                    ntps.append([x , y , model3_grade[1] , 'non_typical_pos'])
                if max_ind == 2:
                    nplus.append([x , y , model3_grade[2] , 'nplus'])

            tps = sorted(tps , key = lambda a : a[2] , reverse = True)
            ntps = sorted(ntps , key = lambda a : a[2] , reverse = True)
            nplus = sorted(nplus , key = lambda a : a[2] , reverse = True)

            if len(tps) > args.anno_nums:
                final_list = tps[ : args.anno_nums]
            else:
                final_list += tps
                left_nums = args.anno_nums - len(tps)
                if len(ntps) > left_nums:
                    final_list += ntps[ : left_nums]
                else:
                    left_nums = left_nums - len(ntps)
                    final_list += nplus[ : left_nums]
            
            # print(len(final_list) , final_list)
            for ite in final_list:
                x = ite[0] - args.m3_bs_r
                y = ite[1] - args.m3_bs_r
                w = args.m3_bs
                h = args.m3_bs
                tid = ite[3] + '_%.4f' % ite[2]
                top50_file.write('%d,%d,%d,%d,%s\n' % (x , y , w , h , tid))
                # tid = '123451'
                # srp.WriteManualAnnoRect(tid, x, y, w, h)

            # srp.close()
            top50_file.close()