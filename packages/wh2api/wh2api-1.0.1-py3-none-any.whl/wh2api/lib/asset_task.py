# -*- coding: utf-8 -*-

import requests


from .. import wh
from . import wh_setting

def list(project_idx,asset_idx):
    api = "/api/project/%s/asset/%s/task/list"%(project_idx,asset_idx)
    api_url = wh.Login.url + api

    # param
    data = ""

    #cookies
    cookies = wh.Login.whtoken

    # api호출
    result = requests.get(api_url, data=data, cookies=cookies)

    #결과확인
    result = wh_setting.result(result)
    return result

def create(project_idx,asset_idx,tasktype_name):
    api = "/api/project/%s/asset/%s/task/create"%(project_idx,asset_idx)
    api_url = wh.Login.url + api

    # param
    data = {"tasktype_name":tasktype_name}

    #cookies
    cookies = wh.Login.whtoken

    # api호출
    result = requests.post(api_url, data=data, cookies=cookies)

    #결과확인
    result = wh_setting.result(result)
    return result

def status_change(project_idx,task_idx,status_idx):
    api = "/api/project/%s/asset/task/%s/status/update"%(project_idx,task_idx)
    api_url = wh.Login.url + api

    # param
    data = {"status_idx":status_idx}

    #cookies
    cookies = wh.Login.whtoken

    # api호출
    result = requests.post(api_url, data=data, cookies=cookies)

    #결과확인
    result = wh_setting.result(result)
    return result


def start(project_idx,task_idx):
    api = "/api/project/%s/asset/task/%s/start"%(project_idx,task_idx)
    api_url = wh.Login.url + api

    # param
    data =""

    #cookies
    cookies = wh.Login.whtoken

    # api호출
    result = requests.post(api_url, data=data, cookies=cookies)

    #결과확인
    result = wh_setting.result(result)
    return result

def stop(project_idx,task_idx):
    api = "/api/project/%s/asset/task/%s/stop"%(project_idx,task_idx)
    api_url = wh.Login.url + api

    # param
    data = ""

    #cookies
    cookies = wh.Login.whtoken

    # api호출
    result = requests.post(api_url, data=data, cookies=cookies)

    #결과확인
    result = wh_setting.result(result)
    return result

