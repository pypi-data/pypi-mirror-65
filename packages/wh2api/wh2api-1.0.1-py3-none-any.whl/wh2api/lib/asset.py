# -*- coding: utf-8 -*-

import requests


from .. import wh
from . import wh_setting

def list(project_idx,category_idx):
    api = "/api/project/%s/category/%s/asset/list"%(project_idx,category_idx)
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


def create(project_idx,category_idx,asset_name,description="",status_idx="1"):
    api = "/api/project/%s/category/%s/asset/create"%(project_idx,category_idx)
    api_url = wh.Login.url + api

    # param
    data = {"asset_name":asset_name,"description":description,"status_idx":status_idx}

    #cookies
    cookies = wh.Login.whtoken

    # api호출
    result = requests.post(api_url, data=data, cookies=cookies)

    #결과확인
    result = wh_setting.result(result)
    return result

def thumbnail_up(project_idx,asset_idx,thumbnail_path):
    api = "/api/project/%s/asset/%s/thumbnail/update"%(project_idx,asset_idx)
    api_url = wh.Login.url + api
    print(thumbnail_path)

    # param
    thumbnail = open(thumbnail_path,'rb')
    data = {"attached":thumbnail}


    #cookies
    cookies = wh.Login.whtoken

    # api호출
    result = requests.post(api_url, files=data, cookies=cookies)

    #결과확인
    result = wh_setting.result(result)
    return result


def overview(project_idx,category_idx=""):
    if category_idx == "":
        api = "/api/project/%s/asset/task/overview/read"%(project_idx)
    else :
        api = "/api/project/%s/category/%s/asset/task/overview/read"%(project_idx,category_idx)
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