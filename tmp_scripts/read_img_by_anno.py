from slide_read_tools.slide_read_factory import srf
from format_conversion.xml_tools import read_xml_by_path

import os
import numpy as np
import cv2

from mysql.sql_con import sql_proxy
from mysql.sql_op import query_slide_info, query_annos, del_anno_by_aid

sql_proxy.connect()


anno_imgs_path = 'L:/GXB/anno_imgs'

# query different group
sql = 'select pro_method, image_method, slide_group, is_positive, zoom \
      from \
      slides \
      group by \
      pro_method, image_method, slide_group, is_positive \
      order by \
      pro_method, image_method, slide_group;'
slide_batches = sql_proxy.execute_query(sql)

log = open(os.path.join(anno_imgs_path, 'log.txt'), 'w')
for slide_batch in slide_batches[2: 4]:
    slides = query_slide_info(pro_method = slide_batch[0], 
                              image_method = slide_batch[1], 
                              slide_group = slide_batch[2], 
                              is_positive = slide_batch[3], 
                              zoom = slide_batch[4])
    print(slide_batch, len(slides))
    
    if len(slides) <= 0:
        continue
    slide_reader = srf.get_proxy(slides[0].slide_format())

    item = '%s__%s__%s__%s__%s' % (slide_batch[0], slide_batch[1], slide_batch[2], 
                                    'Pos' if slide_batch[3] == 'Yes' else 'Neg', slide_batch[4])
    log.write(item + '\t' + str(len(slides)) + '\n')
    cpath = os.path.join(anno_imgs_path, item)
    if not os.path.exists(cpath):
        os.makedirs(cpath)

    for slide in slides:
        annos = query_annos(slide.sid())
        if len(annos) <= 0:
            continue
        # slide_reader = srf.get_proxy(slide.slide_format())
        # slide_reader.open(os.path.join(slide.slide_path(), slide.slide_name()))
        # if not os.path.exists(os.path.join(cpath, slide.slide_name())):
        #     os.makedirs(os.path.join(cpath, slide.slide_name()))

        for anno in annos:
            cir_rect = anno.cir_rect_class()
            if cir_rect.w() > 6000 or cir_rect.h() > 6000 or \
               cir_rect.w() <= 0   or cir_rect.h() <= 0:
            #    del_anno_by_aid(anno.aid())
               log.write(slide.slide_name() + ',' + anno.cir_rect() + '----' + anno.anno_class() + '\n')
               print(slide.slide_name(), anno.cir_rect(), anno.anno_class(), anno.contours_text())
            # try:
            #     img = slide_reader.read_region(cir_rect.x(), cir_rect.y(), cir_rect.w(), cir_rect.h())
            #     if anno.has_contours() == 'Yes':
            #         contours = list()
            #         for contour in anno.contours():
            #             contour[0] -= cir_rect.x()
            #             contour[1] -= cir_rect.y()
            #             contours.append([int(contour[0]), int(contour[1])])
            #         img = cv2.drawContours(img.copy(), np.array([contours]), -1, (0, 0, 255))
                
            #     img_name = anno.cir_rect() + '__' + anno.anno_class() + '.jpg'
            #     cv2.imwrite(os.path.join(cpath, slide.slide_name(), img_name), img)
            # except:
            #     print('slide_name: %s, anno:%s handle failed...' % (slide.slide_name(), 
            #     anno.cir_rect()))
            

# sql_proxy.close()


log.close()