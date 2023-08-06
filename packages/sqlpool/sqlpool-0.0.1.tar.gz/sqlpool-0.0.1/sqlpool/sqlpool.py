import pymysql
import pymssql
from DBUtils.PooledDB import PooledDB


class SQLHandler(object):
    def __init__(self, host, port, user, password, db_name,db_type):
        # pip install --default-timeout=100 dbutils
        self.db_type = db_type
        if db_type == "mysql":
            self.pool = PooledDB(
                # 使用链接数据库的模块import pymysql
                creator=pymysql,
                # 连接池允许的最大连接数，0和None表示不限制连接数
                maxconnections=3,
                # 初始化时，链接池中至少创建的空闲的链接，0表示不创建
                mincached=1,
                # 链接池中最多闲置的链接，0和None不限制
                maxcached=3,
                # 链接池中最多共享的链接数量，0和None表示全部共享。
                # 因为pymysql和MySQLdb等模块的 threadsafety都为1，
                # 所有值无论设置为多少，maxcached永远为0，所以永远是所有链接都共享。
                maxshared=3,
                # 连接池中如果没有可用连接后，是否阻塞等待。True，等待；False，不等待然后报错
                blocking=True,
                # 一个链接最多被重复使用的次数，None表示无限制
                maxusage=None,
                # 开始会话前执行的命令列表。如：["set datestyle to ...", "set time zone ..."]
                setsession=[],
                # ping MySQL服务端，检查是否服务可用。
                #  如：0 = None = never, 1 = default = whenever it is requested,
                # 2 = when a cursor is created, 4 = when a query is executed, 7 = always
                ping=0,

                # 数据库信息
                host=host,
                port=int(port),
                user=user,
                password=password,
                database=db_name,
                charset='utf8',

            )
        elif db_type == "sqlserver":
            self.pool = PooledDB(
                # 使用链接数据库的模块import pymysql
                creator=pymssql,
                # 连接池允许的最大连接数，0和None表示不限制连接数
                maxconnections=5,
                # 初始化时，链接池中至少创建的空闲的链接，0表示不创建
                mincached=2,
                # 链接池中最多闲置的链接，0和None不限制
                maxcached=5,
                # 链接池中最多共享的链接数量，0和None表示全部共享。
                # 因为pymysql和MySQLdb等模块的 threadsafety都为1，
                # 所有值无论设置为多少，maxcached永远为0，所以永远是所有链接都共享。
                maxshared=3,
                # 连接池中如果没有可用连接后，是否阻塞等待。True，等待；False，不等待然后报错
                blocking=True,
                # 一个链接最多被重复使用的次数，None表示无限制
                maxusage=None,
                # 开始会话前执行的命令列表。如：["set datestyle to ...", "set time zone ..."]
                setsession=[],
                # ping MySQL服务端，检查是否服务可用。
                #  如：0 = None = never, 1 = default = whenever it is requested,
                # 2 = when a cursor is created, 4 = when a query is executed, 7 = always
                ping=0,

                # 数据库信息
                host=host,
                user=user,
                password=password,
                database=db_name,
                charset='utf8',

            )

    # def __new__(cls, *args, **kwargs):
    #     if not hasattr(cls, '_instance'):
    #         orig = super(SQLHandler, cls)
    #         cls._instance = orig.__new__(cls)
    #     return cls._instance

    def create_conn_cursor(self):
        # 创建连接
        conn = self.pool.connection()
        # 创建游标
        if self.db_type == "mysql":
            cursor = conn.cursor(pymysql.cursors.DictCursor)
        elif self.db_type == "sqlserver":
            cursor = conn.cursor(as_dict =True)
        else:  #默认是
            cursor = conn.cursor()
        # 返回conn, cursor
        return conn, cursor

    def fetch_one(self, sql, args=None):
        conn, cursor = self.create_conn_cursor()
        cursor.execute(sql, args)
        result = cursor.fetchone()
        cursor.close()
        conn.close()
        return result

    def fetch_many(self, sql, args=None):
        conn, cursor = self.create_conn_cursor()
        cursor.execute(sql)
        result = cursor.fetchmany(args)
        cursor.close()
        conn.close()
        return result

    def fetch_all(self, sql, args=None):
        conn, cursor = self.create_conn_cursor()
        cursor.execute(sql, args)
        result = cursor.fetchall()
        cursor.close()
        conn.close()
        return result

    def insert_one(self, sql, args=None):
        conn, cursor = self.create_conn_cursor()
        res = cursor.execute(sql, args)
        conn.commit()

        conn.close()
        return res

    def insert_many(self, sql, args=None):
        conn, cursor = self.create_conn_cursor()
        res = cursor.executemany(sql, args)
        conn.commit()
        print(res)
        conn.close()
        return res

    def update(self, sql, args=None):
        conn, cursor = self.create_conn_cursor()
        res = cursor.execute(sql, args)
        conn.commit()
        # print(res)
        conn.close()
        return res

    def delete(self, sql, args=None):
        conn, cursor = self.create_conn_cursor()
        res = cursor.execute(sql, args)
        conn.commit()
        print(res)
        conn.close()
        return res
