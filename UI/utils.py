import os
import sqlite3


class DataBase:
    def __init__(self):
        self.con = None
        self.connect_database()
        self.cu = self.con.cursor()

    def creat_database(self):
        self.con.execute("create table test (id integer primary key,img_path varchar(100) NULL, "
                         "fault_img_path varchar(100) NULL,fault_id integer UNIQUE,fault_name varchar(10),datetime "
                         "text NULL, confidence float, fault_x float, fault_y float,fault_w float,fault_h float)")

    def connect_database(self):
        if 'UI' in os.getcwd():
            path = os.getcwd() + '/database/test.db3'
        else:
            path = os.getcwd() + '/UI/database/test.db3'
        if os.path.exists(path):
            need_create = False
        else:
            need_create = True
        self.con = sqlite3.connect(path)
        if need_create:
            self.creat_database()

    # def insert(cu, id='NULL', img_path='NULL', fault_img_path='NULL', fault_id='NULL', fault_name='NULL',
    # datetime='NULL', confidence='NULL', fault_x='NULL', fault_y='NULL', fault_w='NULL', fault_h='NULL'):
    def insert(self, info):
        if len(info) != 11:
            print('插入错误')
            return -1
        # for i, item in enumerate(info):
        #     if item is str:
        #         info[i] = item.decode('utf-8')
        self.cu.execute("INSERT INTO test (id, img_path, fault_img_path, fault_id, fault_name, datetime, "
                            "confidence, fault_x, fault_y, fault_w, fault_h) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);",
                            info)
        self.con.commit()
        return 1

    def delete(self, column_name, value):
        self.cu.execute(f"delete from test where {column_name} = {value}")

    def modify(self, id, column_name, value):
        self.cu.execute(f"update test set {column_name}=? where id = ?", (value, id))

    def search(self, condition=None):
        if condition is not None:
            self.cu.execute(f"select * from test where {condition}")
        else:
            self.cu.execute("select * from test")
        return self.cu.fetchall()  # 如果我们使用cu.fetchone(),则首先返回列表中的第一项,再次使用,则返回第二项,依次下去.


# database = DataBase()
# database.insert((1, 'D', "D", 1, 'hole', '2022.3.12 16:43:29', 0.5608304142951965, 787.90478515625, 257.6526794433594,
#                  53.2989501953125, 60.5352783203125))
# print(database.search())
# database.modify(1, 'fault_name', 'crush')
# print(database.search())
# database.delete('id', 1)
# print(database.search())
