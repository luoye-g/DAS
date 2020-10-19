import os

import sys
sys.path.append('../slide_read_tools/')
sys.path.append('../beans/')
sys.path.append('../mysql/')
from slide_read_factory import srf
from Slide import SlideInfo
from sql_con import MySQLProxy


def get_slide_info(slide_path, slide_format):
    slide_path = slide_path.replace('\\', '/')
    slide_name = slide_path[slide_path.rfind('/') + 1:]
    slide_path = slide_path[: slide_path.rfind('/')]
    print(slide_path, '---', slide_name)

    pro_method = 'Non-BD'
    image_method = slide_path.split('/')[2]
    slide_group = slide_path.split('/')[3]
    zoom = '20x'
    is_positive = 'Yes'
    if slide_path.find('Neg') != -1 or slide_path.find('neg') != -1:
        is_positive = 'No'
    
    mpp, width, height, bounds_x, bounds_y = -1, -1, -1, -1, -1
    # try:
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
    # except:
    #     print(os.path.join(slide_path, slide_name), ' read exception')
    #     zoom = ''

    slide = SlideInfo(slide_path, 
                      slide_name, 
                      slide_group, 
                      pro_method, 
                      image_method, 
                      mpp, 
                      zoom, 
                      slide_format, 
                      '', 
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
                # sql_proxy.insert_into_slides(slide)
        else:
            get_all_slides(current_path, slide_format)


slides_path = 'H:/TCTDATA/SZSQ'
slide_format = 'sdpc'
sql_proxy = MySQLProxy()
sql_proxy.connect()
get_all_slides(slides_path, slide_format)
sql_proxy.close()