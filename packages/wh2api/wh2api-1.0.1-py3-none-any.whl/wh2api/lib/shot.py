# -*- coding: utf-8 -*-

import requests


from .. import wh
from . import wh_setting

def list(project_idx,episode_idx,sequence_idx):
    api = "/api/project/%s/episode/%s/sequence/%s/shot/list"%(project_idx,episode_idx,sequence_idx)
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

def read(project_idx,shot_idx):
    api = "/api/project/%s/shot/%s/read"%(project_idx,shot_idx)
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


def create(project_idx,episode_idx,sequence_idx,shot_name,description="",status_idx="1"):
    api = "/api/project/%s/episode/%s/sequence/%s/shot/create"%(project_idx,episode_idx,sequence_idx)
    api_url = wh.Login.url + api

    # param
    data = {"shot_name":shot_name,"description":description,"status_idx":status_idx}

    #cookies
    cookies = wh.Login.whtoken

    # api호출
    result = requests.post(api_url, data=data, cookies=cookies)

    #결과확인
    result = wh_setting.result(result)
    return result

def thumbnail_up(project_idx,shot_idx,thumbnail_path):
    api = "/api/project/%s/shot/%s/thumbnail/update"%(project_idx,shot_idx)
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


def overview(project_idx,episode_idx=""):
    if episode_idx == "":
        api = "/api/project/%s/shot/task/overview/read"%(project_idx)
    else :
        api = "/api/project/%s/episode/%s/shot/task/overview/read"%(project_idx,episode_idx)
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

def relation(project_idx,episode_idx):
    api = "/api/project/%s/episode/%s/shot/asset/relation/overview/read"%(project_idx,episode_idx)
    api_url = wh.Login.url + api

    # param
    data = ""

    #cookies
    cookies = wh.Login.whtoken

    # api호출
    result = requests.get(api_url, data=data, cookies=cookies)

    #결과확인
    result = wh_setting.result(result)
    return result['overview']