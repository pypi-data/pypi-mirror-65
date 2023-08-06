# -*- coding: utf-8 -*-

import requests
import hashlib
import base64
import json


class Login:
    url =""
    id = ""
    pw = ""
    whtoken = {}
    def __init__(self, wh_url, user_id, user_pw):
        Login.url = wh_url
        Login.id = user_id
        Login.pw = user_pw

        # 웜홀 API URI 세팅
        whtoken_api = "/api/user/auth"  # 웜홀2 API 상세.
        login_api_url = wh_url + whtoken_api

        # 파라미터 확인
        origin_server = wh_url
        outside = "0"

        # 비밀번호 추가 세팅 - 이용자가 입력한 비밀번호를 sha256 해시 후 base64 인코딩 함
        user_pw = user_pw.encode("utf-8")
        user_pw_hashed = hashlib.sha256(user_pw).hexdigest()
        user_pw_hashed = user_pw_hashed.encode("utf-8")
        user_pw_encoded = base64.b64encode(user_pw_hashed)

        # 파라미터 세팅
        data = {"userid": user_id, "userpw": user_pw_encoded, "origin_server": origin_server,
                "outside": outside}

        # API 호출
        login_result = requests.post(login_api_url, data=data)  # JSon형태로 호출

        # 결과 확인 / 토큰 획득
        if login_result.status_code == 200:
            login_result_json = json.loads(login_result.text)
            whtoken = login_result_json["data"]["token"]
            # print(whtoken)

            # 파라미터 세팅
            # whtoken = "eyaoiasddkaso.asodkaosd.asodoasdoas" # 로그인 API 를 통해 얻은 token 값
            Login.whtoken= {"whtoken": whtoken}
            # print(whtoken)
            print('login success')

        else:
            print("login fail")
            # 토큰 획득 실패한 경우