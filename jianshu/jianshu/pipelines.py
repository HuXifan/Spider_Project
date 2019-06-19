# -*- coding: utf-8 -*-
import pymysql
from twisted.enterprise import adbapi  # 专门用来做数据库处理
from pymysql import cursors

# 将爬取的额数据进行持久化存储，当item在spider中被收集后他会被传送到pipeline，
# 一些组件会按照一定的顺序对item执行处理


class JianshuPipeline(object):
    # 存储数据库的方式
    def __init__(self):
        # 创建连接对象
        dbparams = {
            'host': '127.0.0.1',
            'port': 3306,
            'user': 'root',
            'password': 'Root1',
            'database': 'jianshu',
            'charset': 'utf8'  # 编码utf8
        }
        self.conn = pymysql.connect(**dbparams)   # **会把字典的关键字参数插入等价于一下省略的
        # self.conn = pymysql.connect(host='127.0.0.1',)
        self.cursor = self.conn.cursor()  # 创建游标对象
        self._sql = None

    def process_item(self, item, spider):  # 每个item pipeline组件都需要调用的方法
        # item对象是被爬取的item spider对象是代表着爬取该item的spider
        self.cursor.execute(
            self.sql,
            (item['title'],
             item['content'],
                item['author'],
                item['avatar'],
                item['pub_time'],
                item['article_id'],
                item['origin_url']))
        # 执行sql语句，放入参数
        self.conn.commit()  # 提交到数据库中
        return item  # 必须返回一个Item（或者任何继承类）

    @property  # 将方法变成一个属性
    def sql(self):
        if not self._sql:
            self._sql = """
            insert into article(id,title,content,author,avatar,pub_time,article_id,origin_url)
            values (null,%s,%s,%s,%s,%s,%s,%s)
            """
            return self._sql
        return self._sql  # 注意return对其


"""
item pipeline 主要有以下典型应用：
清理HTML数据，
验证爬取的数据的合法性，检查item是否包含某些字段
查重并丢弃
讲爬取结果保存到文件或者数据库中
"""


""" 使用异步插入数据：放在pipeline中，使用twisted提供的数据库连接池connectionPool，
采用同步模式可能会产生阻塞，我们可以使用Twisted将MySQL的入库和解析变成异步操作，
而不是简单的execute，commit同步操作。
"""


# 自定义pipeline,使用Twisted框架实现异步
class JianshuTwistedPipelines(object):
    def __init__(self):
        dbparams = {
            'host': '127.0.0.1',
            'port': 3306,
            'user': 'root',
            'password': 'Root1',
            'database': 'jianshu',
            'charset': 'utf8',  # 编码utf8
            'cursorclass': cursors.DictCursor  # 指定cursor使用哪个类
        }
        # 通过Twisted框架提供的容器连接数据库
        self.dbpool = adbapi.ConnectionPool(
            'pymysql', **dbparams)  # dbapiName  连接池写好
        self._sql = None

    @property  # 将方法变成一个属性
    def sql(self):
        if not self._sql:
            self._sql = """
                insert into article(id,title,content,author,avatar,pub_time,article_id,origin_url,read_count,like_count,word_count,subjects,comment_count)
                values (null,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
                """
            return self._sql
        return self._sql

    def process_item(self, item, spider):
        # runInteraction可以将传入的函数变成异步的
        defer = self.dbpool.runInteraction(self.insert_item, item)
        # 处理异常
        defer.addErrback(self.handle_error, item, spider)

    def insert_item(self, cursor, item):  # 接受游标对象 在使用游标插入数据库
        # 会从dbpool取出cursor
        # 执行具体的插入
        cursor.execute(self.sql,
                       (item['title'],
                        item['content'],
                        item['author'],
                        item['avatar'],
                        item['pub_time'],
                        item['article_id'],
                        item['origin_url'],

                        item['read_count'],
                        item['like_count'],
                        item['word_count'],
                        item['subjects'],
                        item['comment_count']
                        )
                       )
        # 插入mysql的代码从同步变成异步

    def handle_error(self, error, item, spider):  # 处理异步插入的异常
        print("=" * 10 + 'error' + '=' * 10)
        print(error)
        print("=" * 10 + 'error' + '=' * 10)
