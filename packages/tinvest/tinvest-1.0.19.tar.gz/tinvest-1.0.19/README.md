# T-Invest

[![Build Status](https://api.travis-ci.com/daxartio/tinvest.svg?branch=master)](https://travis-ci.com/daxartio/tinvest)
[![PyPI](https://img.shields.io/pypi/v/tinvest)](https://pypi.org/project/tinvest/)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/tinvest)](https://www.python.org/downloads/)
[![Codecov](https://img.shields.io/codecov/c/github/daxartio/tinvest)](https://travis-ci.com/daxartio/tinvest)
[![GitHub last commit](https://img.shields.io/github/last-commit/daxartio/tinvest)](https://github.com/daxartio/tinvest)
[![Tinvest](https://img.shields.io/github/stars/daxartio/tinvest?style=social)](https://github.com/daxartio/tinvest)

```
pip install tinvest
```

Данный проект представляет собой инструментарий на языке Python для работы с OpenAPI Тинькофф Инвестиции, который можно использовать для создания торговых роботов.

Клиент предоставляет синхронный и асинхронный API для взаимодействия с Тинькофф Инвестиции.

## Начало работы

### Где взять токен аутентификации?

В разделе инвестиций вашего  [личного кабинета tinkoff](https://www.tinkoff.ru/invest/) . Далее:

* Перейдите в настройки
* Проверьте, что функция "Подтверждение сделок кодом" отключена
* Выпустите токен для торговли на бирже и режима "песочницы" (sandbox)
* Скопируйте токен и сохраните, токен отображается только один раз, просмотреть его позже не получится, тем не менее вы можете выпускать неограниченное количество токенов

## Документация

Документацию непосредственно по OpenAPI можно найти по [ссылке](https://api-invest.tinkoff.ru/openapi/docs/).

### Быстрый старт

Для непосредственного взаимодействия с OpenAPI нужно создать клиента. Клиенты разделены на streaming и rest.

Примеры использования SDK находятся ниже.

### У меня есть вопрос

[Основной репозиторий с документацией](https://github.com/TinkoffCreditSystems/invest-openapi/) — в нем вы можете задать вопрос в Issues и получать информацию о релизах в Releases.
Если возникают вопросы по данному SDK, нашёлся баг или есть предложения по улучшению, то можно задать его в Issues.

## Примеры:

Для работы с данным пакетом вам нужно изучить OpenAPI Тинькофф Инвестиции [ссылка](https://api-invest.tinkoff.ru/openapi/docs/)

```python
import asyncio

import tinvest

TOKEN = "<TOKEN>"

events = tinvest.StreamingEvents()


@events.candle()
async def handle_candle(
    api: tinvest.StreamingApi, payload: tinvest.CandleStreamingSchema
):
    print(payload)


@events.orderbook()
async def handle_orderbook(
    api: tinvest.StreamingApi, payload: tinvest.OrderbookStreamingSchema
):
    print(payload)


@events.instrument_info()
async def handle_instrument_info(
    api: tinvest.StreamingApi, payload: tinvest.InstrumentInfoStreamingSchema
):
    print(payload)


@events.error()
async def handle_error(
    api: tinvest.StreamingApi, payload: tinvest.ErrorStreamingSchema
):
    print(payload)


@events.startup()
async def startup(api: tinvest.StreamingApi):
    await api.candle.subscribe("BBG0013HGFT4", tinvest.CandleResolution.min1)
    await api.orderbook.subscribe("BBG0013HGFT4", 5, "123ASD1123")
    await api.instrument_info.subscribe("BBG0013HGFT4")


@events.cleanup()
async def cleanup(api: tinvest.StreamingApi):
    await api.candle.unsubscribe("BBG0013HGFT4", "1min")
    await api.orderbook.unsubscribe("BBG0013HGFT4", 5)
    await api.instrument_info.unsubscribe("BBG0013HGFT4")


async def main():
    await tinvest.Streaming(TOKEN, state={"postgres": ...}).add_handlers(events).run()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass

```

```python
import tinvest

TOKEN = "<TOKEN>"

client = tinvest.SyncClient(TOKEN)
api = tinvest.PortfolioApi(client)

response = api.portfolio_get()  # requests.Response
if response.status_code == 200:
    print(response.parse_json())  # tinvest.PortfolioResponse
```

```python
# Handle error
...
api = tinvest.OperationsApi(client)

response = api.operations_get("", "")
if response.status_code != 200:
    print(response.parse_error())  # tinvest.Error
```

```python
import asyncio
import tinvest

TOKEN = "<TOKEN>"

client = tinvest.AsyncClient(TOKEN)
api = tinvest.PortfolioApi(client)


async def request():
    async with api.portfolio_get() as response:  # aiohttp.ClientResponse
        if response.status == 200:
            print(await response.parse_json())  # tinvest.PortfolioResponse


loop = asyncio.get_event_loop()
loop.run_until_complete(request())
```