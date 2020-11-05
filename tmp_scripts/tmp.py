# delete later
# coding: gbk
import os
import xlrd
import shutil
import cv2
from mysql.sql_op import query_slide_info
from slide_read_tools.slide_read_factory import srf


group_dict = {'tj4':    'Tongji_4th', 
              'tj4n':   'Tongji_4th', 
              'tj5':    'Tongji_5th', 
              'tj6':    'Tongji_6th', 
              'tj7':    'Tongji_7th'
}

save_path = 'L:/GXB/fql_on/slides'
slide_path = 'H:/TCTDATA/SZSQ/Shengfuyou_8th/positive/pos_ascus/sfy1615617 2226087.sdpc'
slide_read = srf.get_proxy('sdpc')

slide_read.open(slide_path)

item = '03__sfy8p__sfy1615617 2226087__nplus__nplus-16__keep__keep__72067__5667__415__415__'
x = 72067 - int(415 / 2)
y = 5667 - int(415 / 2)
w = 415
h = 415
img = slide_read.read_region(x, y, w, h)
cv2.imwrite('t.jpg', img)
slide_read.close()