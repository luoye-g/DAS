from slide_read_tools.slide_read_factory import srf
from format_conversion.xml_tools import read_xml_by_path

import os
import numpy as np
import cv2

xml_path = 'H:/TCTDATA/SZSQ/Labelfiles/xml_Tongji_6th'
sli_path = 'H:/TCTDATA/SZSQ/Tongji_6th/positive'
sli_form = 'sdpc'
name = 'tj19062677'
level = 0

annos, _ = read_xml_by_path(os.path.join(xml_path, name + '.xml'))

srr = srf.get_proxy(sli_form)
srr.open(os.path.join(sli_path, name + '.' + sli_form))
for anno in annos:
    x = anno.cir_rect_class().x()
    y = anno.cir_rect_class().y()
    w = anno.cir_rect_class().w()
    h = anno.cir_rect_class().h()
    img = srr.read_region(x, y, w, h, )
    print(np.shape(img))
    cv2.imwrite(anno.cir_rect() + '.png', img)
srr.close()


