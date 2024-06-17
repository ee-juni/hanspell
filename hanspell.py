# -*- coding: utf-8 -*-
"""
Python용 한글 맞춤법 검사 모듈
Originally from https://github.com/ssut/py-hanspell.git
Source: https://github.com/kw-lee/alfhanspell/blob/main/workflow/hanspell_break.py
"""

import requests
import json
import sys
import xml.etree.ElementTree as ET
import re
from urllib import parse
import os
from datetime import datetime, timezone, timedelta

base_url = 'https://m.search.naver.com/p/csearch/ocontent/util/SpellerProxy'

_agent = requests.Session()
PY3 = sys.version_info[0] == 3

def get_kr_date():
    KST = timezone(timedelta(hours=9))
    time_record = datetime.now(KST)
    return str(time_record)[:10]

def read_token():
    if os.path.isfile("token.txt"):
        with open("token.txt", "r") as f:
            DATE, TOKEN = list(map(lambda x: x.strip(), f.readlines()))
        if get_kr_date() == DATE:
            return TOKEN
        else:
            TOKEN = update_token(_agent)
    else:
        TOKEN = update_token(_agent)
    return TOKEN

def update_token(agent):
    """update passportkey
    from https://gist.github.com/AcrylicShrimp/4c94db38b7d2c4dd2e832a7d53654e42
    """
    
    html = agent.get(url='https://search.naver.com/search.naver?where=nexearch&sm=top_hty&fbm=1&ie=utf8&query=맞춤법검사기') 

    match = re.search('passportKey=([a-zA-Z0-9]+)', html.text)
    if match is not None:
        TOKEN = parse.unquote(match.group(1))
        with open("token.txt", "w") as f:
            f.write(get_kr_date() + "\n")
            f.write(TOKEN)
    return TOKEN

def _remove_tags(text):
    text = u"<content>{}</content>".format(text).replace("<br>", "\n")
    # 띄어쓰기 그대로 사용
    if not PY3:
        text = text.encode("utf-8")

    result = "".join(ET.fromstring(text).itertext())

    return result

def _get_data(text, token):
    payload = {
        "q": text,
        "color_blindness": 0,
        "passportKey": token
    }
    headers = {
        "Host": "m.search.naver.com",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.9 Safari/537.36",
        "referer": "https://search.naver.com/",
        "Accept-Language": "ko-KR,ko;q=0.8,en-US;q=0.5,en;q=0.3",
        "Accept": "*/*"
    }
    r = _agent.get(base_url, params=payload, headers=headers)
    data = json.loads(r.text)
    return data

def get_correction(text):
    TOKEN = read_token()
    data = _get_data(text, TOKEN)
    if "error" in data["message"].keys():
        TOKEN = update_token(_agent)
        data = _get_data(text, TOKEN)
        if "error" in data["message"].keys():
            return "맞춤법 검사가 불가능합니다."
    html = data["message"]["result"]["html"]
    return _remove_tags(html)

