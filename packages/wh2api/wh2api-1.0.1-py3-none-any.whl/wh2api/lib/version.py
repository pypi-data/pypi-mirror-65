# -*- coding: utf-8 -*-

import requests


from .. import wh
from . import wh_setting


def key(task_idx, which='shot or asset'):
    api = "/api/%s/task/%s/version/setting/create"%(which,task_idx)
    api_url = wh.Login.url + api

    # param
    data = ""

    #cookies
    cookies = wh.Login.whtoken

    # api호출
    result = requests.post(api_url, data=data, cookies=cookies)

    #결과확인
    result = wh_setting.result(result)
    return result['version_key']

def key_read(version_key):
    api = "/api/version/setting/read"
    api_url = wh.Login.url + api

    # param
    data = {'version_key':version_key}

    #cookies
    cookies = wh.Login.whtoken

    # api호출
    result = requests.post(api_url, data=data, cookies=cookies)

    #결과확인
    result = wh_setting.result(result)
    return result

def create(task_idx,which,version_name,task_status_idx,version_status_idx,reviewer_user_idx,hour_spent,version_path):
    version_key = key(task_idx,which)
    key_data = key_read(version_key)

    api = "/api/%s/task/version/create"%(which)
    api_url = wh.Login.url + api

    # param

    data = {"which":which,
             "version_key":version_key,
             "project_idx":key_data['project_idx'],
             "version_name":version_name,
             "task_status_idx":task_status_idx,
             "version_status_idx":version_status_idx,
             "hour_spent":hour_spent,
             "reviewer_user_idx":reviewer_user_idx,
             "main_path":version_path,
             "attached_path[]":version_path}
    if which =="shot" :
        shot_data={"episode_idx": key_data['episode_idx'],
                   "sequence_idx": key_data['sequence_idx'],
                   "shot_idx": key_data['shot_idx']}
        data.update(shot_data)
    elif which =="asset":
        asset_data={"asset_category_idx": key_data['asset_category_idx'],
                    "asset_idx": key_data['asset_idx']}
        data.update(asset_data)
    else:
        print("which error")


    print(data)
    file = {"attached[]":open(version_path,'rb')}

    #cookies
    cookies = wh.Login.whtoken

    # api호출
    result = requests.post(api_url, data=data,files=file, cookies=cookies)

    #결과확인
    result = wh_setting.result(result)
    return result