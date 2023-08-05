# !/usr/bin/env python
# _*_coding: utf-8 _*_
# @Time: 2019/10/17 17:52
# @Author: "John"
import pymongo

import bson
import os
import shutil
import sys
import traceback
from datetime import datetime

from pymongo import MongoClient

"""
    模板作用： 
        1、main_function 这个方法，提供对指定《数据库》中的指定《表》进行循环查询，将查询出来的 document，传递到 core_logic 中进行处理
        2、core_logic 这个方法由调用 data_fix_main 的用户自己完成，必须有三个参数；
        3、本模板，可以通过 pip install zy-tools 直接调用，不必拷贝过来拷贝过去
"""


# 只需传入文件名称，自动生成以当前脚本名称为前缀的 .txt 文件，保存到相对路径下，作为日志文件。
def data_fix_logger(msg, fl_name='', mode="a", need_time=True, need_log=True):
    if not need_log:
        return

    time_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger_file_name = os.path.basename(sys.argv[0])[:-3] + fl_name + ".log"
    with open(logger_file_name, mode) as f:
        if need_time:
            f.write(time_str + ' => ')
        f.write(msg)
        f.write("\n")


# 获取文件最后一个合法的 _id，用于断点续读
def get_last_id(file_name):
    with open(file_name, 'r') as f:

        index = -1
        while True:
            _id = f.readlines()[index].strip()
            if len(_id) == 24:
                return _id

            data_fix_logger(f"Get the {-index} th _id error; Current _id: {_id}")
            index -= 1


def find_documents(conn, data_base, collection, query, projection, sort_key="_id", sort_value=pymongo.ASCENDING, limits=0):
    # 默认根据_id 升序排列，不限制返回的结果数量
    _docs = conn[data_base][collection].find(query, projection).sort(sort_key, sort_value).limit(limits)
    # 将结果集放到一个 list 中，方便计数
    docs = [item for item in _docs]
    return docs


def core_logic_example(conn, document, is_sandbox):
    """
    核心处理逻辑样例，调用者自己实现。
    【注意】必须有且仅有这三个参数

    :param conn:
    :param document:
    :param is_sandbox:
    :return:
    """
    pass


def data_fix_main(uri, db, collection, more_filter, projections, core_logic, starts='', end_id='', quit_limit=0, limits=500, is_sandbox=True):
    """

    :param uri: MongoDB 的账号信息
    :param db:  MongoDB 库名
    :param collection: MongoDB 表名
    :param more_filter: 查询 filter
    :param projections: 查询 projection
    :param core_logic: 核心逻辑，需调用者自己实现一个方法，且这个方法有且只能有两个参数，分别是 MongoDB 连接对象，和查出来的 document
    :param starts: 起始 _id ， 可以不提供
    :param end_id: 终点 _id ， 可以不提供
    :param quit_limit: 处理 document 的数量限制，达到后程序结束，用于定量测试程序的运行；默认为0， 不做限制
    :param limits: MongoDB 每次查询返回文档的限制，默认为 500
    :param is_sandbox: 是否是测试状态，默认是 True
    :return:
    """

    start_id = ''
    current_id = ''
    exception_count = 0
    has_query_count = 0
    has_read_id_count = 0
    conn = MongoClient(uri)
    current_file_name = os.path.basename(sys.argv[0])[:-3]

    # 如果存在断点文件，先复制保存一份，再继续使用该文件，防止发生错误，无法从之前的断点继续
    old_logger_file = f"{current_file_name}_has_read_{collection}_ids.log"
    if os.path.exists(old_logger_file):
        try:
            log_date = str(datetime.now().date())
            log_time = str(datetime.now().time())[:-7]
            bak_up_file_time = (log_date + '_' + log_time).replace('-', '_').replace(':', '_')
            shutil.copy(old_logger_file, f"{current_file_name}_has_read_{collection}_ids_{bak_up_file_time}.log")
            start_id = get_last_id(old_logger_file)
        except Exception as e:
            msg = str(e) + ",trace:" + traceback.format_exc()
            data_fix_logger(f"Failed to get last id, exit! Error Msg {msg}.")
            sys.exit()

    # 读取数据库中的第一条 _id
    if not start_id:
        one_doc = conn[db][collection].find(more_filter, projection={"_id": 1}).sort("_id", pymongo.ASCENDING)
        start_id = one_doc[0]["_id"]
        data_fix_logger(str(start_id), fl_name=f'_has_read_{collection}_ids', mode='w', need_time=False)

    query = {"_id": {"$gte": bson.ObjectId(start_id)}}

    # 传入起点，则以传入的 objectId 为起点，否则以库中查询的第一条或者读取本地文件。
    if starts:
        query = {"_id": {"$gte": bson.ObjectId(starts)}}

    if more_filter:
        query.update(more_filter)

    # 捕获异常20 次，则退出检查
    while exception_count < 20:

        has_query_count += 1
        docs = find_documents(conn, db, collection, query, projections, "_id", pymongo.ASCENDING, limits)
        fl = "_query_db_counts"
        log_msg = f"****** Has queried {collection}: {has_query_count}*{limits}={has_query_count*limits}  documents. *******"
        data_fix_logger(log_msg, fl_name=fl, mode="w")

        try:
            # 查询结果为空，直接退出
            if not docs:
                data_fix_logger(f"Empty doc, exit! Last _id is: {current_id}.")
                return

            for doc in docs:

                has_read_id_count += 1
                current_id = _id = doc.get("_id")
                query["_id"] = {"$gt": current_id}
                data_fix_logger(str(start_id), fl_name=f'_has_read_{collection}_ids', mode='w', need_time=False)

                # 给定退出限制， 达到限制的额时候，退出程序；
                # 不给 quit_limit 传递值的时候，则不会在这里判断
                if quit_limit and has_read_id_count > quit_limit:
                    data_fix_logger(f"Get end point, and mission is over! Last _id is: {current_id}.")
                    sys.exit()

                # 程序退出条件 2
                if end_id and (current_id > end_id):
                    data_fix_logger(f"Get end point, and mission is over! Last _id is: {current_id}.")
                    sys.exit()  # 程序退出

                # 核心处理逻辑
                core_logic(conn, doc, is_sandbox)

        except Exception as e:
            query["_id"] = {"$gt": current_id}  # 新的query
            data_fix_logger(f'Get error, exception msg is {str(e) + ",trace:" + traceback.format_exc()}, current _id is: {current_id}.')
            exception_count += 1

    data_fix_logger(f"Catch exception 20 times, mission is over. Last _id is: {current_id}.")
