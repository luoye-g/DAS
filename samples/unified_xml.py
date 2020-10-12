import os

from format_conversion.xml_tools import read_xml_by_slide, save_xml_slide_anno
from mexception import SlideError

out_path = 'H:/TCTDATA'
pro_method = 'Non-BD'
image_method = '3D'

slide_group = 'Shengfuyou_1th'
slide_forma = 'mrxs'
format_trans = None
is_positive = 'Yes'
x = '20x'
sub_class = None
is_hard = 'No'
sli_path = os.path.join(out_path, '3DHistech/Shengfuyou_1th/Positive')
xml_path = os.path.join(out_path, '3DHistech/Shengfuyou_1th/Labelfiles/Xml')

unified_xml_path = 'E:/desktop/fql_on/unified_xml'
xmls = [x for x in os.listdir(xml_path) if x.find('.xml') != -1]

concrete_path = os.path.join(unified_xml_path,
                             image_method,
                             slide_group,
                             'Positive' if is_positive is 'Yes' else 'Negative')
if not os.path.exists(concrete_path):
    os.makedirs(concrete_path)

# convert xml to unified xml
for k, xml in enumerate(xmls):
    if k < 150:
        continue
    slide_name = xml[: xml.find('.xml')]
    s_path = os.path.join(sli_path, slide_name + '.' + slide_forma)
    x_path = os.path.join(xml_path, xml)
    print(k, slide_name)
    try:
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
    except(SlideError):
        print('slide read error!')
