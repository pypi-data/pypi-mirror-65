# Проект Python-клиента для dmz-nats-bridge

## Использование
Для использования клиентского модуля необходимо:
1. Скопировать файл bridge_client.py в основной проект
2. В основной проект установить библиотеку
```
pipenv install nats-python
```
Пример кода:
```python
from bridge_client import BridgeClient, BridgeResponse, BridgeRequest
import logging

class SampleOneRequest(BridgeRequest):
    def __init__(self):
        super().__init__()
        self.Name: str = ''

one = SampleOneRequest()
one.Name = "Вася"

logger = logging.getLogger()

client = BridgeClient(logger, 'nats://nats-client.k8s.vitebsk.energo.net:4222', 10)
result: dict = client.send_and_recive('sample.one', one)
```


