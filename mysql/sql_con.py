
import MySQLdb

HOST = 'localhost'
USER = 'gxb'
PASSWORD = '1181895140'
DB = 'das'
CHARSET = 'utf8'


class MySQLProxy:

    def __init__(self):
        self._db = None
        pass

    def connect(self):
        self._db = MySQLdb.connect(host=HOST, user=USER, password=PASSWORD, db=DB, charset=CHARSET)

    def execute_query(self, sql):
        try:
            cursor = self._db.cursor()
            results = cursor.execute(sql)
            return results
        except:
            print(sql, ' excute failed ... ')
            self._db.rollback()
            return None


    def close(self):
        if self._db is not None:
            self._db.close()

    
    def insert_into_class_code(self, data):
        sql = '''
                insert into class_code 
                (code, class, anno)
                values
                ('%s', '%s', '%s')
        '''\
        % (data['code'], data['class'], data['anno'])
        cursor = self._db.cursor()
        # try:
        cursor.execute(sql)
        self._db.commit()
        # except:
        #     print('insert into class_code error')
        #     self._db.rollback()

    def insert_into_slide_sub_class(self, data):
        '''
        ��slide_sub_class���в�������
        :param data: ������֯��ʽΪ�ֵ�
        :return:
        '''
        # print(data)
        sql = """insert into slide_sub_class
        (slide_name, slide_group, slide_format, pro_method, image_method, age, Medical_history, sub_class, 
        remarks, is_positive)
        VALUES 
        ('%s', '%s', '%s', '%s', '%s', %s, '%s', '%s', '%s', '%s');
        """ % (data['slide_name'], data['slide_group'], data['slide_format'], data['pro_method'],
               data['image_method'], data['age'], data['Medical_history'], data['sub_class'],
               data['remarks'], data['is_positive'])
        # print(sql)
        cursor = self._db.cursor()
        # try:
        cursor.execute(sql)
        self._db.commit()
        # except:
        #     print('error')
        #     self._db.rollback()

    def create_slide_sub_class(self):
        '''
        ����slide_sub_class��
        :return:
        '''
        create_table_sql = '''
                    create table slide_sub_class (
                    id int not null auto_increment,
                    slide_name varchar(60) not null,
                    slide_group varchar(50),
                    slide_format varchar(20),
                    pro_method varchar(20),
                    image_method varchar(20),
                    age int,
                    Medical_history varchar(60),
                    sub_class varchar(60),
                    primary key (id)
                    )
                    '''
        cursor = self._db.cursor()
        cursor.execute(create_table_sql)

    def create_slide_hard(self):
        '''
        ����������Ƭ��
        :return:
        '''
        create_table_sql = '''
                       create table slide_hard (
                       id int not null auto_increment,
                       slide_name varchar(60) not null,
                       slide_group varchar(50),
                       slide_format varchar(20),
                       pro_method varchar(20),
                       image_method varchar(20),
                       is_positive varchar(10),
                       slide_classify_score float,
                       pos_num int,
                       recon_num int,
                       jppos_22 int,
                       full_anno varchar(60),
                       sub_class varchar(60),
                       p_10_5Num int,
                       primary key (id)
                       )
                       '''
        cursor = self._db.cursor()
        cursor.execute(create_table_sql)

    def insert_into_slides(self, slide):
        sql = """insert into slides
          (slide_path, slide_name, slide_group, pro_method, image_method, mpp, zoom, 
          slide_format, is_positive, width, height, bounds_x, bounds_y, format_trans)
          VALUES 
          ('%s', '%s', '%s', '%s', '%s', %s, '%s', '%s', '%s', %s, %s, %s, %s, '%s');
          """ % (slide.slide_path(), slide.slide_name(), slide.slide_group(), slide.pro_method(),
                 slide.image_method(), slide.mpp(), slide.zoom(), slide.slide_format(),
                 slide.is_positive(), slide.width(), slide.height(), slide.bounds_x(), slide.bounds_y(), 
                 slide.format_trans())
        try:
            cursor = self._db.cursor()
            cursor.execute(sql)
            self._db.commit()
        except(MySQLdb._exceptions.IntegrityError):
            self._db.rollback()
            print('data duplicate ..... ')

    def insert_into_annotations(self, data, anno):
        query_sql = 'select sid from slides where slide_path = \'%s\' and slide_name = \'%s\'' \
        % (data['slide_path'], data['slide_name'])
        cursor = self._db.cursor()
        cursor.execute(query_sql)
        # 获取所有记录列表
        results = cursor.fetchall()
        sid = 0
        for row in results:
            sid = row[0]
        
        insert_sql = """insert into annotations
          (sid, center_point, cir_rect, anno_class, anno_code, type, \
            color, is_typical, contours, is_hard) \
            VALUES \
            (%d, '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s');""" % \
          (sid, anno['center_point'], anno['cir_rect'], anno['anno_class'], anno['anno_code'],
                anno['type'], anno['color'], anno['is_typical'], anno['contours'], anno['is_hard'])
        try:
            cursor.execute(insert_sql)
            self._db.commit()
        except:
            if len(anno['contours']) > 10000:
                print('contours too long')
            else:
                print('data duplicate ....')
            self._db.rollback()
    def insert_into_slide_hard(self, data):
        '''
          ��slide_hard���в�������
          :param data: ������֯��ʽΪ�ֵ�
          :return:
          '''
        # print(data)
        sql = """insert into slide_hard
          (slide_name, slide_group, slide_format, pro_method, image_method, is_positive, 
          slide_classify_score, pos_num, recon_num, jppos_22, full_anno, sub_class, p_10_5Num)
          VALUES 
          ('%s', '%s', '%s', '%s', '%s', '%s', %s, %s, %s, %s, '%s', '%s', %s);
          """ % (data['slide_name'], data['slide_group'], data['slide_format'], data['pro_method'],
                 data['image_method'], data['is_positive'], data['slide_classify_score'], data['pos_num'],
                 data['recon_num'], data['jppos_22'], data['full_anno'], data['sub_class'], data['p_10_5Num'])
        print(sql)
        cursor = self._db.cursor()
        # try:
        cursor.execute(sql)
        self._db.commit()
        # except:
        #     print('error')
        #     self._db.rollback()

# # get cursor
# cursor = db.cursor()
# create_table_sql = '''CREATE TABLE EMPLOYEE (
#                          FIRST_NAME  CHAR(20) NOT NULL,
#                          LAST_NAME  CHAR(20),
#                          AGE INT,
#                          SEX CHAR(1),
#                          INCOME FLOAT )'''
# cursor.execute(create_table_sql)
# db.close()
import os
from format_conversion.xml_tools import *


def concret_xml(xml_path):
    
    xmls = os.listdir(xml_path)
    for xml in xmls:
        current_path = os.path.join(xml_path, xml)
        if xml.find('.xml') != -1:
            print(current_path)
            slide_info, annos, _ = read_xml_slide_anno(current_path)
            data = dict()
            data['slide_path'] = slide_info.slide_path().replace('\\', '/')
            data['slide_name'] = slide_info.slide_name()
            data['slide_group'] = slide_info.slide_group()
            data['pro_method'] = slide_info.pro_method()
            data['image_method'] = slide_info.image_method()
            data['mpp'] = slide_info.mpp()
            data['zoom'] = slide_info.zoom()
            data['slide_format'] = slide_info.slide_format()
            data['is_positive'] = slide_info.is_positive()
            data['width'] = slide_info.width()
            data['height'] = slide_info.height()
            data['bounds_x'] = slide_info.bounds_x()
            data['bounds_y'] = slide_info.bounds_y()
            for anno in annos:
                anno_dict = dict()
                anno_dict['center_point'] = anno.center_point()
                anno_dict['cir_rect'] = anno.cir_rect()
                anno_dict['anno_class'] = anno.anno_class()
                anno_dict['anno_code'] = anno.anno_code()
                anno_dict['type'] = anno.type()
                anno_dict['color'] = anno.color()
                anno_dict['is_typical'] = anno.is_typical()
                anno_dict['is_hard'] = 'No'
                if current_path.find('hard') != -1:
                    anno_dict['is_hard'] = 'Yes'
                contours = ''
                for contour in anno.contours():
                    contours += (str(contour[0]) + ',' + str(contour[1]) + ';')
                anno_dict['contours'] = contours
                # print(anno_dict)
                sql_proxy.insert_into_annotations(data, anno_dict)
        else:
            concret_xml(current_path)

sql_proxy = MySQLProxy()
# def read_all_xml(xmls_path):
#     concret_xml(xmls_path)
#
#
# if __name__ == '__main__':
#
#     sql_proxy = MySQLProxy()
#     sql_proxy.connect()
#     read_all_xml('L:/GXB/unified_xml')
#     sql_proxy.close()