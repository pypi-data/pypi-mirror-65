# -*- coding: utf-8 -*-
import json


# 결과 확인
def result(result):

    if result.status_code == 200:
        json_list = json.loads(result.text)['data']
        print(json.loads(result.text)['error']['message'])
        return json_list
    else:
        errorcode = "errorcode:"+str(result.status_code)
        print(errorcode)
        return errorcode