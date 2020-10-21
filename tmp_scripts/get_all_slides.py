import os

import sys
from slide_read_tools.slide_read_factory import srf
from beans.Slide import SlideInfo
from mysql.sql_con import MySQLProxy


def get_slide_info(slide_path, slide_format):
    slide_path = slide_path.replace('\\', '/')
    slide_name = slide_path[slide_path.rfind('/') + 1:]
    slide_path = slide_path[: slide_path.rfind('/')]

    pro_method = 'BD'
    image_method = slide_path.split('/')[2]
    slide_group = slide_path.split('/')[3]
    if slide_path.find('Not_BD') != -1:
        pro_method = 'Non-BD'

    zoom = '20x'
    is_positive = 'Yes'
    if slide_path.find('Neg') != -1 or slide_path.find('neg') != -1:
        is_positive = 'No'
    
    mpp, width, height, bounds_x, bounds_y = -1, -1, -1, -1, -1
    try:
        sr = srf.get_proxy(slide_format)
        sr.open(os.path.join(slide_path, slide_name))

        mpp = sr.mpp()
        if float(mpp) < 0.2:
            zoom = '40x'
        width = sr.width()
        height = sr.height()
        bounds_x = sr.boundsx()
        bounds_y = sr.boundsy()

        sr.close()
    except:
        read_slide_log.write(os.path.join(slide_path, slide_name) + '\t read exception\n')
        print(os.path.join(slide_path, slide_name), ' read exception')
        zoom = ''

    print(slide_path, '---', slide_name, ' ', mpp)
    slide = SlideInfo(slide_path, 
                      slide_name, 
                      slide_group, 
                      pro_method, 
                      image_method, 
                      mpp, 
                      zoom, 
                      slide_format, 
                      'NULL', 
                      is_positive, 
                      '', 
                      width, 
                      height, 
                      '',
                      bounds_x, 
                      bounds_y)
    # slide.show_info()
    return slide


def get_all_slides(slides_path, slide_format = 'mrxs'):


    slides = os.listdir(slides_path)
    
    for slide in slides:
        current_path = os.path.join(slides_path, slide)
        if os.path.isfile(current_path):
            if current_path.endswith(slide_format):
                # slide_read_proxy.open(current_path)
                # slide_read_proxy.close()
                slide = get_slide_info(current_path, slide_format)
                sql_proxy.insert_into_slides(slide)
        else:
            get_all_slides(current_path, slide_format)


read_slide_log = open('./read_slides.log', 'a+')

slides_path = 'H:/TCTDATA/BD'
slide_format = 'srp'
sql_proxy = MySQLProxy()
sql_proxy.connect()
get_all_slides(slides_path, slide_format)
sql_proxy.close()
read_slide_log.close()