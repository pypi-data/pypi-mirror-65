# -*- coding: utf-8 -*-

import requests

from . import wh_setting
from .. import wh


def todo(observed_user_idx=""):

    api = "/api/mytask/todo/read"
    api_url = wh.Login.url + api

    # param
    data = ""

    #cookies
    cookies = wh.Login.whtoken
    if observed_user_idx != "":
        cookies["observed_user_idx"] =observed_user_idx

    # api호출
    result = requests.get(api_url, data=data, cookies=cookies)

    #결과확인
    result = wh_setting.result(result)
    return result


def inprogress(last=""):

    api = "/api/mytask/inprogress/read/%s"%(last)
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

def done():

    api = "/api/mytask/done/read"
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

def cc(last=""):

    api = "/api/mytask/cc/read/%s"%(last)
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