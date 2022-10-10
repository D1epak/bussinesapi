### Business API SDK python - Библиотека написанная для взаимодействия с бизнес.ru
Что бы начать работу с api, нужно подключить библиотеку
```python
from assets.api import BusinessApi
```
Далее нужно объявить класс BusinessApi, и передать в него секретный ключ и ID приложения
```python
from assets.api import BusinessApi

test = BusinessApi("секретный ключ", "ID приложения")
```
Где test, это переменная хранящая в себе параметры и позволяющая работать с api.

Более подробно можете узнать на сайте самого бизнес api.
https://app.swaggerhub.com/apis/Business.Ru/check.business.ru/2.0.0#/
https://api-online.class365.ru/api-polnoe/vvedenie_v_api_biznesru/228