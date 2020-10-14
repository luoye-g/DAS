import os

import sys
sys.path.append('../format_conversion')
from xml_tools import read_xml_by_slide, save_xml_slide_anno
from mexception import SlideError

out_path = 'H:/TCTDATA'
pro_method = 'BD'
image_method = 'BD'

slide_group = 'Tongji_11th'
slide_forma = 'srp'
format_trans = None
is_positive = 'Yes'
x = '20x'
sub_class = None
is_hard = 'No'
sli_path = os.path.join(out_path, 'BD/Tongji_11th/positive/BD')
xml_path = os.path.join(out_path, 'BD/Tongji_11th/Labelfiles/BD')

unified_xml_path = 'L:/GXB/unified_xml'
xmls = [x for x in os.listdir(xml_path) if x.find('.xml') != -1]

concrete_path = os.path.join(unified_xml_path,
                             image_method,
                             slide_group,
                             'Positive' if is_positive is 'Yes' else 'Negative')
if not os.path.exists(concrete_path):
    os.makedirs(concrete_path)

# convert xml to unified xml
for k, xml in enumerate(xmls):
    # if k <= 0:
    #     continue
    slide_name = xml[: xml.find('.xml')]
    s_path = os.path.join(sli_path, slide_name + '.' + slide_forma)
    x_path = os.path.join(xml_path, xml)
    print(k, slide_name)
    # try:
    slide_info, annos = read_xml_by_slide(x_path,
                                            s_path,
                                            slide_group,
                                            pro_method,
                                            image_method,
                                            x,
                                            format_trans=format_trans,
                                            is_positive=is_positive,
                                            sub_class=sub_class,
                                            is_hard=is_hard)
    save_xml_slide_anno(slide_info, annos, os.path.join(concrete_path, xml))
    # except(SlideError):
    #     print('slide read error!')
    # break