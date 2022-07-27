# -*- encoding: utf-8 -*-
"""
@File    :   rdbms.py    
@Contact :   puyongjun@flashhold.com
@License :   (C)Copyright 2021-2025

@Modify Time      @Author    @Version    @Desciption
------------      -------    --------    -----------
2021/8/5 11:02   parker      1.0         操作数据库
"""
import logging
import time

from sqlalchemy import create_engine
from sqlalchemy.engine import CursorResult
from sqlalchemy.orm import sessionmaker

from startmap.utils.str import gen_md5

Logger = logging.getLogger(__file__)


class MyRDBMS:
    """
    用来操作 RDBMS
    """
    db_session = None
    engine = None

    def __init__(self, db_type="MYSQL", *args, **kwargs):
        """
        打开的时候传入参数
        :param db_type:
        :param args:
        :param kwargs:
        """
        conn_url = None
        if str(db_type).upper() == "MYSQL":
            conn_url = "mysql+pymysql://{user}:{password}@{host}:{port}/{db}?charset=utf8".format(**kwargs)

        self.engine = create_engine(
            url=conn_url,
            pool_pre_ping=True,  # 悲观机制
            pool_size=20,  # 连接池
            max_overflow=0, # 连接多久断开
            # pool_recycle=1800,  # 超过30分钟空闲会回收
            # pool_pre_ping=True,  # 预检测池中连接是否有效，并替换无效连接
            pool_use_lifo=True,  # 使用后进先出的方式获取连接，允许多余连接保持空闲
            echo_pool=True,  # 会打印输出连接池的异常信息，帮助排查问题
            # echo=True  # 开启SQL输出
        )
        # 创建会话的类
        self.db_session = sessionmaker(bind=self.engine)

    def execute(self, *args, **kwargs) -> CursorResult:
        """
        执行
        :param args:
        :param kwargs:
        :return:
        """
        with self.db_session() as db:
            data = db.execute(*args, **kwargs)
            db.commit()
            return data

    def save_data(self, table_name: str, pk: (tuple, list), data_rows: (tuple, list), i=0) -> bool:
        """
        保存数据到数据库
        :param table_name: 表名
        :param pk: 主键名
        :param data_rows: 数据
        :param i: 重试次数
        :return:
        """
        # 如果超过次数或者是没有数据，就直接返回
        i += 1
        if i > 3 or len(data_rows) < 1:
            return False

        # 数据去重
        new_data_rows = []
        for __li in data_rows:
            if __li not in new_data_rows:
                new_data_rows.append(__li)

        try:
            self.__save_data(table_name, pk, new_data_rows)
        except Exception as e:
            print(e)
            time.sleep(1)
            self.save_data(table_name, pk, new_data_rows, i)

    def __save_data(self, table_name: str, pk: (tuple, list), data_rows: (tuple, list)):
        """
        执行插入与更新
        :param table_name: 表名
        :param pk: 主键
        :param data_rows: 数据
        :return:
        """
        # 获取要插入的 key
        column_arr = []
        for __line in data_rows:
            column_arr.extend(__line.keys())
        column_arr = set(column_arr)

        # 查询数据是否存在
        def gen_pk_md5_data(__pk_line: dict, value_type="db"):
            key_data = []
            for k in pk:
                key_data.append(__pk_line.get(k))

            if value_type == "db":
                return "'{}'".format(gen_md5("##".join(key_data)))
            return gen_md5("##".join(key_data))

        exist_data = self.execute("select {pk_md5} from {table_name} where {pk_md5} in({value_md5})".format(
            table_name=table_name,
            pk_md5="MD5(CONCAT({}))".format(",'##',".join(pk)),
            value_md5=",".join(map(gen_pk_md5_data, data_rows)),
        ))

        # 定义需要插入与更新的数据
        exist_key, insert_data, update_data = [], [], []
        for __line_result_key in exist_data:
            exist_key.extend(__line_result_key)

        for __line_data in data_rows:
            if gen_pk_md5_data(__line_data, value_type="str") in exist_key:
                update_data.append(__line_data)
            else:
                insert_data.append(__line_data)

        Logger.info("insert {},update {}".format(len(insert_data), len(update_data)))
        print("insert {},update {}".format(len(insert_data), len(update_data)))
        self.insert_data(table_name=table_name, column_arr=column_arr, data=insert_data) if insert_data else None
        self.update_data(table_name=table_name, column_arr=column_arr, pk=pk, data=update_data) if update_data else None

    def insert_data(self, table_name: str, column_arr: (tuple, list), data: (tuple, list)):
        """
        插入数据
        :param table_name: 表名
        :param column_arr: 列名
        :param data: 数据
        :return:
        """
        # 获取要插入的 key
        if not column_arr:
            column_arr = []
            for __line in data:
                column_arr.extend(__line.keys())
            column_arr = set(column_arr)

        self.execute(
            "INSERT INTO {table_name} ({column}) VALUES ({value})".format(
                table_name=table_name,
                column=",".join(column_arr),
                value=",".join(map(lambda x: ":{}".format(x), column_arr))),
            data
        ) if data else None

        # 存入统计
        self.collection_static(static_type="insert_data", data=data)

    def update_data(self, table_name: str, column_arr: (tuple, list), pk: (tuple, list), data: (tuple, list)):
        """
        更新数据
        :param table_name: 表名
        :param column_arr: 列名
        :param pk: 主键
        :param data: 数据
        :return:
        """
        # 获取要插入的 key
        if not column_arr:
            for __line in data:
                column_arr.extend(__line.keys())
            column_arr = set(column_arr)

        for __update_line in data:
            self.execute(
                "UPDATE {table_name} SET {key_tuple} WHERE {pk}".format(
                    table_name=table_name,
                    key_tuple=",".join(map(lambda x: "{x}=:{x}".format(x=x), column_arr)),
                    pk=" AND ".join(map(lambda x: "{x}=:{x}".format(x=x), pk)),
                ),
                __update_line
            ) if __update_line else None

        # 存入统计
        self.collection_static(static_type="update_data", data=data)

    def collection_static(self, static_type, *args, **kwargs):
        """
        预留的保留函数
        :param static_type: 统计类型
        :param args:
        :param kwargs:
        :return:
        """
        pass

    def __del__(self):
        """
        关闭的时候清理
        :return:
        """
        if self.db_session:
            self.db_session.close_all()
