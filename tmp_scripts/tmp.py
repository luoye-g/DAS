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
slide_path = 'H:/TCTDATA/SZSQ/XiaoYuWei_1th/positive/052910070.sdpc'
slide_read = srf.get_proxy('sdpc')

slide_read.open(slide_path)

item = '03__hardslide__052910070__pos__atypical-02__keep__keep__14110__84460__138__275__.jpg'
w = 138
h = 275
x = 14110 + int(512 * 0.293 / 0.17817 / 2) - int(w / 2)
y = 84460 + int(512 * 0.293 / 0.17817 / 2) - int(w / 2)
img = slide_read.read_region(x, y, w, h)
cv2.imwrite('t.jpg', img)
slide_read.close()