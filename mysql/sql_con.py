
import MySQLdb

HOST = 'localhost'
# USER = 'gxb'
# PASSWORD = '1181895140'
USER = '***'
PASSWORD = '***'
DB = 'das'
CHARSET = 'utf8'


class MySQLProxy:

    def __init__(self):
        self._db = None
        pass

    def connect(self):
        self._db = MySQLdb.connect(host=HOST, user=USER, password=PASSWORD, db=DB, charset=CHARSET)


    def exceute_update(self, sql):
        try:
            cursor = self._db.cursor()
            cursor.execute(sql)
            self._db.commit()
        except:
            print(sql, ' excute failed ... ')
            self._db.rollback()


    def execute_query(self, sql):
        try:
            cursor = self._db.cursor()
            cursor.execute(sql)
            results = cursor.fetchall()
            return results
        except:
            print(sql, ' excute failed ... ')
            self._db.rollback()
            return None

    def close(self):
        if self._db is not None:
            self._db.close()

    
    def create_table_ANNO_DETECTION(self):
        create_table_sql = '''
                            CREATE TABLE `anno_detection` (
                            `id` bigint NOT NULL AUTO_INCREMENT,
                            `aid` bigint NOT NULL,
                            `detection_box` varchar(100) DEFAULT NULL,
                            PRIMARY KEY (`id`),
                            UNIQUE KEY `aid_UNIQUE` (`aid`)
                            ) ENGINE=InnoDB AUTO_INCREMENT=48930 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci
                            '''
        self.exceute_update(create_table_sql)

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
        query_sql = '''select sid from slides where slide_name = '%s' and slide_group='%s'
        and pro_method='%s' and image_method='%s' and zoom = '%s' and is_positive='%s';''' \
        % (data['slide_name'], data['slide_group'], data['pro_method'], data['image_method'], 
        data['zoom'], data['is_positive'])
        cursor = self._db.cursor()
        cursor.execute(query_sql)
        # 获取所有记录列表
        results = cursor.fetchall()
        sid = 0
        for row in results:
            sid = row[0]
        assert sid != 0
        insert_sql = """insert into annotations
          (sid, center_point, cir_rect, anno_class, anno_code, type, \
            color, is_typical, contours, is_hard) \
            VALUES \
            (%d, '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s');""" % \
          (sid, anno['center_point'], anno['cir_rect'], anno['anno_class'], anno['anno_code'],
                anno['type'], anno['color'], anno['is_typical'], anno['contours'], anno['is_hard'])
        if len(anno['contours']) > 15000:
            print('insert data toot long ....')
        try:
            cursor.execute(insert_sql)
            self._db.commit()
        except:
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
    
sql_proxy = MySQLProxy()