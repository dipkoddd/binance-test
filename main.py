from binance.websocket.spot.websocket_client import SpotWebsocketClient as WebsocketClient
from datetime import datetime, timedelta


last_message_sent_at = datetime.fromtimestamp(0)


def updates_handler(message: dict):  # Обработчик всех обновлений с вебсокета
    global last_message_sent_at
    percent = message.get("P")  # Процент на который изменилась максимальная цена за последний час
    price_change = message.get("p")  # На сколько изменилась цена
    symbol = message.get("s")  # Название пары

    if percent is not None and price_change is not None and symbol is not None:  # На всякий случай проверяем что объявленные выше переменные не пустые
        if float(percent) <= -1.0 and datetime.now() > last_message_sent_at+timedelta(minutes=1):  # Если процент изменения максимальной цены меньше 1.0% и последнее сообщение было более часа назад
            print(f"Цена на пару {symbol} изменилась на {percent} ({price_change})")  # Выводим сообщение
            last_message_sent_at = datetime.now()  # Записываем во сколько последнее сообщение было получено чтобы консоль не спамила


ws_client = WebsocketClient()
ws_client.start()

ws_client.rolling_window_ticker(
    windowSize="1h",
    callback=updates_handler,
    id=1,
    symbol="XRPUSDT",
    type="MINI"
)
