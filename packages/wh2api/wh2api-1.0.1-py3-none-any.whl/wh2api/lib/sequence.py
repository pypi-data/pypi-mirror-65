# -*- coding: utf-8 -*-

import requests

from .. import wh
from . import wh_setting

def list(project_idx,episode_idx):
    api = "/api/project/%s/episode/%s/sequence/list"%(project_idx,episode_idx)
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

def create(project_idx,episode_idx,sequence_name,description=""):
    api = "/api/project/%s/episode/%s/sequence/create"%(project_idx,episode_idx)
    api_url = wh.Login.url + api

    # param
    data = {"sequence_name":sequence_name,"description":description}

    #cookies
    cookies = wh.Login.whtoken

    # api호출
    result = requests.post(api_url, data=data, cookies=cookies)

    #결과확인
    result = wh_setting.result(result)
    return result