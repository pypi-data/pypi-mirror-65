import re
from io import BytesIO
from tempfile import gettempdir
from zipfile import ZipFile

import requests
import pandas as pd
from functools import wraps


class cache(object):
    def __init__(self, seconds=-1):
        self.seconds = seconds
        self.latest_dt = None
        self.cache = None

    def __call__(self, func, *args, **kwargs):
        @wraps(func)
        def func_wrap(*args, **kwargs):
            if self.cache is not None:
                return self.cache

            self.cache = func(*args, **kwargs)
            return self.cache

        return func_wrap


class Dart(object):
    def __init__(self, api_key: str):
        self.api_key = api_key
        self._tmp_dir = gettempdir()

    @cache(seconds=1)
    def get_corp_codes(self) -> pd.DataFrame:
        """
        회사의 고유번호를 모두 가져옵니다.
        :return:
        """
        res = requests.get('https://opendart.fss.or.kr/api/corpCode.xml',
                           params=dict(crtfc_key=self.api_key))
        zipfile = ZipFile(BytesIO(res.content))
        filename = zipfile.namelist()[0]
        corp_text = zipfile.open(filename).read().decode()
        corp_text = corp_text.split('\n')

        tag_regex = re.compile(r'<(corp_code|corp_name|stock_code|modify_date)>(.*)</\1>')
        corps = []
        corp = {}
        for i, line in enumerate(corp_text):
            line = line.strip()
            match = tag_regex.match(line)
            if match:
                if match.group(1).startswith('corp_c'):
                    if corp:
                        corps.append(corp)
                    corp = {}
                corp[match.group(1)] = match.group(2)

        return pd.DataFrame(corps)
