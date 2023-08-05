# !/usr/bin/env python
# _*_coding: utf-8 _*_
# @Time: 2019/6/24 11:23
# @Author: "John"

from aliyun.log.getlogsrequest import GetLogsRequest


def query_log(client, query, project='java-crawler', log_store='reaper_log', query_start_time=0, query_end_time=0, line=100000):
    query_result = None

    while (not query_result) or (not query_result.is_completed()):
        rest = GetLogsRequest(project, log_store, query_start_time, query_end_time, "", query, reverse=True, line=line)
        query_result = client.get_logs(rest)

    return query_result.get_body()
