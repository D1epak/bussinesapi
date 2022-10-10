import json
import typing
import uuid
from hashlib import md5
from random import choice
from string import digits, ascii_letters
from typing import Dict

import requests


class BusinessApi:
    """
        При отправке запроса к API приложение должно выполнить ряд действий.

        К массиву параметров запроса добавляются параметры: nonce, app_id и token, где
        -- nonce - случайно генерируемая, уникальная для каждого запроса строка,
        -- app_id - уникальный идентификатор, выданный при подключении интеграции на аккаунте,
        -- token - полученный токен интеграции.
        Полученный массив параметров сортируется в алфавитном порядке и преобразуется в json строку - params_string.
        К запросу добавляется заголовок sign. Подпись запроса вычисляется по формуле: sign = MD5( params_string + secret ),
        где параметром функции MD5 служит конкатенация компонентов:
        -- params_string - url-кодированная строка параметров
        -- secret - секретный ключ, полученный при подключении интеграции на аккаунте.
    """

    def __init__(self, secret_key, app_id):
        """
        Init - метод конструктор собирает библиотеку для работы.
        :param secret_key: секретный ключ, полученный при подключении интеграции на аккаунте.
        :param app_id: уникальный идентификатор, выданный при подключении интеграции на аккаунте.
        :param nonce: случайно генерируемая, уникальная для каждого запроса строка.
        """
        self.secret_key = secret_key
        self.app_id = app_id
        self.nonce = "".join(choice(digits + ascii_letters) for _ in range(10))

    @staticmethod
    def get_sign(secret: str, param: dict) -> str:
        """
        Создание уникальной подписи для каждого запроса.
            Вернет сгенерированную подпись из параметров запроса.
        :param secret:
        :param param:
        :return:
        """
        params_string = json.dumps(param).replace(' ', '')
        string = params_string + secret
        return md5(string.encode("utf-8")).hexdigest()

    @staticmethod
    def get_unique_hashcat():
        hashcat_one = uuid.uuid4()
        hashcat_two = uuid.uuid4()
        type_to_string = str(hashcat_one) + str(hashcat_two)
        hashcat = md5(type_to_string.encode("utf-8")).hexdigest()
        return hashcat

    def get_token(self):
        """
        Получение и восстановление токена.
            Вернёт новый токен если его нет, если есть то текущий токен.
        """
        try:
            param: Dict = {"app_id": self.app_id, "nonce": self.get_unique_hashcat()}
            sign = self.get_sign(self.secret_key, param)
            headers = {'Content-type': 'application/json; charset=utf-8',
                       'Accept': 'application/json', 'sign': sign}
            response = requests.get(url="https://check.business.ru/open-api/v1/Token/", params=param, headers=headers)
            data = response.json()
            token = json.dumps(data["token"])
            return token.strip('""')
        except Exception as error:
            print(error)

    def get_user(self):
        """
        Работа с пользователем / аккаунтом
            Вернет информацию о текущем пользователе / аккаунте
        """
        param: Dict = {"app_id": self.app_id, "nonce": self.nonce, "token": self.get_token()}
        sign = self.get_sign(self.secret_key, param)

        headers = {'Content-type': 'application/json; charset=utf-8',
                   'Accept': 'application/json', 'sign': sign}
        response = requests.get(url="https://check.business.ru/open-api/v1/User/", params=param, headers=headers)
        data = response.json()
        print(data)

    def get_command_id(self, **kwargs):
        """
        Получение данных о команде в ФР по ID пользователя и ID команды
            Вернёт информацию о команде ФР
                Подробнее можно узнать на:

                https://app.swaggerhub.com/apis/Business.Ru/check.business.ru/2.0.0#/JSON_check

                https://app.swaggerhub.com/apis/Business.Ru/check.business.ru/2.0.0#/JSON_shift

                https://app.swaggerhub.com/apis/Business.Ru/check.business.ru/2.0.0#/JSON_cash

                https://app.swaggerhub.com/apis/Business.Ru/check.business.ru/2.0.0#/JSON_report

                https://app.swaggerhub.com/apis/Business.Ru/check.business.ru/2.0.0#/JSON_correction

                https://app.swaggerhub.com/apis/Business.Ru/check.business.ru/2.0.0#/Shifts

                https://app.swaggerhub.com/apis/Business.Ru/check.business.ru/2.0.0#/Checks

                https://app.swaggerhub.com/apis/Business.Ru/check.business.ru/2.0.0#/Goods
        """
        param: Dict = {"app_id": self.app_id, "nonce": self.nonce, "token": self.get_token()}
        sign = self.get_sign(self.secret_key, param)

        headers = {'Content-type': 'application/json; charset=utf-8',
                   'Accept': 'application/json', 'sign': sign}
        response = requests.get(url="https://check.business.ru/open-api/v1/Command/{}".format(kwargs), params=param,
                                headers=headers)
        data = response.json()
        print(data)

    def get_command(self, filter_date_create_from, filter_date_create_to, filter_date_update_from,
                    filter_date_update_to, filter_date_result_from, filter_date_result_to, page, c_num):
        """
        Получение данных о команде в ФР по ID пользователя и ID команды
            Вернёт информацию о команде ФР с учётом фильтров
        """
        param: Dict = {"app_id": self.app_id,
                       "filter_date_create_from": filter_date_create_from,
                       "filter_date_create_to": filter_date_create_to,
                       "filter_date_update_from": filter_date_update_from,
                       "filter_date_update_to": filter_date_update_to,
                       "filter_date_result_from": filter_date_result_from,
                       "filter_date_result_to": filter_date_result_to,
                       "page": page,
                       "c_num": c_num,
                       "nonce": self.nonce,
                       "token": self.get_token(),
                       }

        headers = {'Content-type': 'application/json; charset=utf-8',
                   'Accept': 'application/json', 'sign': self.get_unique_sign()}
        response = requests.get(url="https://check.business.ru/open-api/v1/Command", params=param,
                                headers=headers)
        data = response.json()
        print(data)

    def get_state_system(self):
        """
        Получение данных о состоянии системы.
            Вернёт информацию о текущем состоянии системы.
        """
        param: Dict = {"app_id": self.app_id, "nonce": self.nonce, "token": self.get_token()}
        sign = self.get_sign(self.secret_key, param)

        headers = {'Content-type': 'application/json; charset=utf-8',
                   'Accept': 'application/json', 'sign': sign}
        response = requests.get(url="https://check.business.ru/open-api/v1/StateSystem/", params=param, headers=headers)
        data = response.json()
        return data

    def get_shift(self, filter_date_create_from, filter_date_create_to, filter_date_update_from,
                  filter_date_update_to, filter_date_result_from, filter_date_result_to, page, c_num):
        """
        Получение данных о сменах.
            Вернёт информацию о сменах с учётом фильтров.
        """
        param: Dict = {"app_id": self.app_id,
                       "filter_date_create_from": filter_date_create_from,
                       "filter_date_create_to": filter_date_create_to,
                       "filter_date_update_from": filter_date_update_from,
                       "filter_date_update_to": filter_date_update_to,
                       "filter_date_result_from": filter_date_result_from,
                       "filter_date_result_to": filter_date_result_to,
                       "page": page,
                       "c_num": c_num,
                       "nonce": self.nonce,
                       "token": self.get_token(),
                       }
        sign = self.get_sign(self.secret_key, param)

        headers = {'Content-type': 'application/json; charset=utf-8',
                   'Accept': 'application/json', 'sign': sign}
        response = requests.get(url="https://check.business.ru/open-api/v1/Shift/", params=param, headers=headers)
        data = response.json()
        return data