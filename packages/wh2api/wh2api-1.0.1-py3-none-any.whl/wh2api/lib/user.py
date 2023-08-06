# -*- coding: utf-8 -*-

import requests

from .. import wh
from . import wh_setting

def list():

    api = "/api/user/list"
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