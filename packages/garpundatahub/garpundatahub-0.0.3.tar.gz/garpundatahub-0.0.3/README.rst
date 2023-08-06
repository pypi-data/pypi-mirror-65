Garpun Datahub Python Library
=============================

|build| |pypi|

.. |build| image:: https://travis-ci.org/garpun/garpun-datahub-lib-python.svg?branch=master
   :target: https://travis-ci.org/garpun/garpun-datahub-lib-python
.. |pypi| image:: https://img.shields.io/pypi/v/garpundatahub.svg
   :target: https://pypi.python.org/pypi/garpundatahub

garpundatahub - это клиентская библиотека для доступа к данным пользователя Garpun.
Включает в себя класс для обработки данных с помошью Pandas.

Получение ключа сервисного аккаунта
-----------------------------------

Для начала работы с библиотекой вам необходимо получить json файл с
ключом от сервисного аккаунта. Если у вас его ещё нет воспользуйтесь
этой `инструкцией <https://cloud.garpun.com/authenticate/service_account/>`__.

Установка garpundatahub
-----------------------

Поддерживается Python >= 3.6 Поддерживаемые операционные системы: OSX, Windows, Ubuntu.

Внимание! Для использования функий оперирующих с типом DataFrame
необходимо дополнительно установить pandas==1.0.3

``pip3 install garpundatahub --upgrade --no-cache``

Примеры
-------

Полный список примеров вы можете найти в `репозитории <https://github.com/garpun/garpun-datahub-lib-python/tree/master/examples>`__

Пример использования
--------------------

.. code:: python

    from garpundatahub.client import DataHubClient
    from garpundatahub.datahub import DataHub
    from pandas import DataFrame

    # Берем настройки из файла.
    # Переполучение access токена будет выполняться внутри библиотеки, не требуя вашего участия. 
    api_client = DataHubClient.from_service_account_file("../creds.json")
    garpun_datahub = DataHub(api_client=api_client)

    # metaql запрос. Подробнее  https://cloud.garpun.com/api_datahub/metaql/
    query = "select id, name from adplatform.client" 

    # Скачиваем файл в формате newline json
    garpun_datahub.download_query_to_disk(query)

    # Загружаем данные в пандас, если данных нет, или они устарели, они будут скачаны заново. 
    df: DataFrame = garpun_datahub.json_to_df(query)

