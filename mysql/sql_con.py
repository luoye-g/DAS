# coding=gbk
import MySQLdb

HOST = 'localhost'
USER = 'root'
PASSWORD = '1181895140'
DB = 'das'
CHARSET = 'utf8'


class MySQLProxy:

    def __init__(self):
        self._db = None
        pass

    def connect(self):
        self._db = MySQLdb.connect(host=HOST, user=USER, password=PASSWORD, db=DB, charset=CHARSET)

    def close(self):
        if self._db is not None:
            self._db.close()

    def insert_into_slide_sub_class(self, data):
        '''
        向slide_sub_class表中插入数据
        :param data: 数据组织方式为字典
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
        创建slide_sub_class表
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
        创建困难切片表
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

    def insert_into_slide_hard(self, data):
        '''
          向slide_hard表中插入数据
          :param data: 数据组织方式为字典
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

# if __name__ == '__main__':
#
#     sql_proxy = MySQLProxy()
#     sql_proxy.connect()
#     sql_proxy.create_slide_hard()