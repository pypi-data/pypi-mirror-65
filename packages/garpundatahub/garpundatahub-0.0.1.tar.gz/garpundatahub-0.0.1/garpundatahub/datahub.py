import hashlib
import json
import re
import shutil
from os import path
from tempfile import gettempdir
from datetime import datetime, timedelta, timezone
from typing import List

import requests
from requests import Response
from yaml import load as yaml_load, dump as yaml_dump
from yaml import Loader, Dumper

MIN_EXPIRE_TIME = 20

garpun_to_pandas_type = {

    "UNKNOWN": "object",
    "TEXT": "string",
    "BOOLEAN": "bool",

    "PERCENT": "float64",
    "DECIMAL": "float64",

    # case have matter!
    # Int64: https://pandas.pydata.org/pandas-docs/version/0.24/whatsnew/v0.24.0.html#optional-integer-na-support
    # https://youtrack.jetbrains.com/issue/PY-34650
    "INT": "float64",
    "LONG": "float64",

    "DATE": "object",
    "TIME": "object",
    "DATETIME": "object"
}


class DataHub(object):
    def __init__(self, api_client):
        self.call_metaql = api_client.call_metaql

    @staticmethod
    def __parse_type_in_headers(headers: dict) -> dict:
        if not headers.get("X-Meta-Column-Types"):
            return {}
        columns_type: dict = json.loads(headers["X-Meta-Column-Types"])
        dtype = {}
        convert_dates = []
        for garpun_type, columns in columns_type.items():
            if garpun_type in ("DATE", "TIME", "DATETIME"):
                convert_dates.extend(columns)

            for column in columns:
                dtype[column] = garpun_to_pandas_type.get(garpun_type, "object")

        return {"dtype": dtype, "convert_dates": convert_dates}

    @staticmethod
    def __unic_query_name(query: str) -> str:
        pattern = re.compile(r"\s+")
        query = re.sub(pattern, " ", query)
        table_name = query.lower().split(" from ")[-1].split(" ")[0].strip()
        query_md5 = hashlib.md5(query.encode("utf-8")).hexdigest()
        pattern = re.compile(r"[^a-zA-Z0-9#_]")
        table_name = re.sub(pattern, "_", table_name)
        return table_name + "__" + query_md5

    @staticmethod
    def __is_time_expired(yaml_data: dict) -> bool:
        now = datetime.now(timezone.utc)
        return now >= (yaml_data.get("expiration_time", now) if yaml_data else now)

    def __save_response_to_file(self, *, response: Response, pathfile: str, save_metadata: bool, expire_limit: int) -> None:
        with open(pathfile + ".json.gz", "wb") as out_file:
            shutil.copyfileobj(response.raw, out_file)

        if save_metadata:
            metadata = {
                "pandas_types": self.__parse_type_in_headers(response.headers),
                "expiration_time": datetime.now(timezone.utc) + timedelta(minutes=expire_limit),
                "expire_limit": expire_limit
            }
            with open(pathfile + ".yaml", "w") as file:
                yaml_dump(metadata, file, Dumper)

    def download_feed_to_disk(self, feed_key: str, pathfile: str = None, from_data: str = None, to_data: str = None, hint_fields: List[str] = None) -> str:
        """
        :param feed_key:
        :param pathfile:
        :param from_data:
        :param to_data:
        :param hint_fields:
        :return:
        """
        query_string = {
            "from": from_data,
            "to": to_data,
            "hint_fields": ",".join(hint_fields) if hint_fields else None
        }
        url = f"https://datahub-api.garpun.com/v1/feeds/stream_feed/{feed_key}"

        response = requests.post(url=url,
                                 stream=True,
                                 params={k: v for k, v in query_string.items() if v}
                                 )

        if not pathfile:
            pathfile = path.join(gettempdir(), feed_key.split("/")[0])

        self.__save_response_to_file(
            response=response,
            pathfile=pathfile,
            save_metadata=False,
            expire_limit=0
        )
        return pathfile

    def download_query_to_disk(self, query: str, pathfile: str = None, save_metadata: bool = True, expire_limit: int = 30, shard_key: int = None) -> str:
        """
        Принимает запрос и скачивает данные на диск.

        :param query: Запрос в формате metaql.
        :param pathfile: Путь до файла с данными, без расширения. Например  ~/data/stats
                         Если не передан, то файлы сохраняются в системную временную папку.
                         Вместе с json файлом также будет сохранен yaml файл с типами данных колонок в формате pandas
        :param save_metadata: Нужно ли сохранять файл с метаданными запроса.
        :param expire_limit: Через сколько минут считать файл с данными устаревшим.
        :param shard_key: Идентификатор шарды. Обязательный параметр для запросов ....todo
        :return:
        """
        if MIN_EXPIRE_TIME > expire_limit:
            raise Exception(f"expire_limit cannot be less than {MIN_EXPIRE_TIME}")

        response: Response = self.call_metaql(query, shard_key)

        if not pathfile:
            pathfile = path.join(gettempdir(), self.__unic_query_name(query))

        self.__save_response_to_file(
            response=response,
            pathfile=pathfile,
            save_metadata=save_metadata,
            expire_limit=expire_limit
        )

        return pathfile

    def json_to_df(self, query: str, pathfile: str = None, shard_key: int = None):
        """
        Принимает запрос и если необоходимо скачивает данные с сервера.

        :param query: Запрос в формате metaql.
        :param pathfile: Путь до файла с данными, без расширения. Например  ~/data/stats
                         Если не передан, то файлы сохраняются в системную временную папку.
                         Вместе с json файлом также будет сохранен yaml файл с типами данных колонок в формате pandas
        :param shard_key: Идентификатор шарды. Обязательный параметр для запросов ....todo
        :return: pd.DataFrame
        """
        try:
            from pandas import read_json
        except ImportError:
            raise ImportError("For use this function you should install pandas==1.0.3")

        if not pathfile:
            pathfile = path.join(gettempdir(), self.__unic_query_name(query))

        try:
            with open(pathfile + ".yaml", "r") as file:
                yaml_data = yaml_load(file, Loader=Loader)
        except FileNotFoundError:
            yaml_data = {}

        if self.__is_time_expired(yaml_data):
            self.__save_response_to_file(
                response=self.call_metaql(query, shard_key),
                pathfile=pathfile,
                save_metadata=True,
                expire_limit=yaml_data.get("expire_limit", 30)
            )

        # https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.read_json.html
        settings = {
            "path_or_buf": pathfile + ".json.gz",
            "orient": "records",
            "lines": True,
            "compression": "gzip",
            "date_unit": "ms",
            "keep_default_dates": False
        }

        settings.update(**yaml_data.get("pandas_types", {}))
        return read_json(**settings)
