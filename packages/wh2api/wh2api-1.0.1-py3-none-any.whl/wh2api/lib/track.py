# -*- coding: utf-8 -*-

import requests

from .. import wh
from . import wh_setting

def version(project_idx,from_date="yyyy-mm-dd",to_date="yyyy-mm-dd",last=""):
    #last = "" or "last"

    api = "/api/project/%s/track/from/%s/to/%s/version/read/%s"%(project_idx,from_date,to_date,last)
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

