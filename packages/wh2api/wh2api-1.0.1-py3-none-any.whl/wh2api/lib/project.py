# -*- coding: utf-8 -*-

import requests

from .. import wh
from . import wh_setting

def list(finished=""):
    # finished = '1' 끝난 프로젝트도 조회

    api = "/api/project/list"
    api_url = wh.Login.url + api

    # param
    data = {"including_finished": finished, "all": "1"}

    #cookies
    cookies = wh.Login.whtoken

    # api호출
    result = requests.get(api_url, data=data, cookies=cookies)

    #결과확인
    result = wh_setting.result(result)
    return result

def read(project_idx):
    api = "/api/project/%s/detail/read"%(project_idx)
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