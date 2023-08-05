import json
import inspect
import threading
import time
import uuid
from logging import Logger

from pynats import NATSClient, NATSMessage, NATSSubscription  # type: ignore
from typing import List


class ObjectEncoder(json.JSONEncoder):
    def default(self, obj):
        if hasattr(obj, "to_json"):
            return self.default(obj.to_json())
        elif hasattr(obj, "__dict__"):
            d = dict(
                (key, value)
                for key, value in inspect.getmembers(obj)
                if not key.startswith("__")
                and not inspect.isabstract(value)
                and not inspect.isbuiltin(value)
                and not inspect.isfunction(value)
                and not inspect.isgenerator(value)
                and not inspect.isgeneratorfunction(value)
                and not inspect.ismethod(value)
                and not inspect.ismethoddescriptor(value)
                and not inspect.isroutine(value)
            )
            return self.default(d)
        return obj


class BridgeRequest:
    def __init__(self):
        self.Id = uuid.uuid4().hex


class BridgeResponse:
    def __init__(self):
        self.Id: str = ''
        self.IsError: bool = False
        self.Error: str = ''


class Attachment:
    def __init__(self):
        self.Name = ''
        self.Base64Body = ''


class SendEmailRequest(BridgeRequest):
    def __init__(self):
        super().__init__()
        self.RecipientName: str = ''
        self.RecipientAddress: str = ''
        self.Subject: str = ''
        self.TextMessage: str = ''
        self.Attachments: List[Attachment] = []


class SendEmailResponse(BridgeResponse):
    def __init__(self):
        super().__init__()


class SendSmsRequest(BridgeRequest):
    def __init__(self):
        super().__init__()
        self.Description: str = ''
        self.RecipientPhone: str = ''
        self.Message: str = ''


class SendSmsResponse(BridgeResponse):
    def __init__(self):
        super().__init__()


class BridgeClient:
    __uri: str
    __socket_timeout: float
    __log: Logger

    def __init__(self, log: Logger, uri: str, socket_timeout: float) -> None:
        self.__uri = uri
        self.__socket_timeout = socket_timeout
        self.__log = log

    def send_and_recive(self, subject: str, request: BridgeRequest) -> dict:
        result: List[dict] = []
        self.__log.debug(f'send_and_recive() subject:{subject}')

        def worker():
            try:
                self.__log.debug(f'worker()')
                with NATSClient(self.__uri, socket_timeout=self.__socket_timeout) as subscription_client:
                    subscription_subject = BridgeClient._get_subscription_subject(subject, request.Id)

                    def callback(msg: NATSMessage) -> None:
                        try:
                            res: dict = json.loads(msg.payload)
                            self.__log.debug(f'callback() subject:{subject}')
                            result.append(res)
                        except Exception as ex:
                            self.__log.error(str(ex))
                    self.__log.debug(f'subscription_client.subscribe() subscription_subject:{subscription_subject}')
                    subscription: NATSSubscription = subscription_client.subscribe(
                        subscription_subject, callback=callback)
                    subscription_client.wait(count=1)
                    self.__log.debug(f'subscription_client.wait ...OK')
            except Exception as e:
                err_res = BridgeResponse()
                err_res.Id = request.Id
                err_res.IsError = True
                err_res.Error = str(e)
                result.append(json.loads(json.dumps(err_res, cls=ObjectEncoder)))
                self.__log.error(str(e))

        t = threading.Thread(target=worker)
        t.start()
        time.sleep(1)

        with NATSClient(self.__uri, socket_timeout=self.__socket_timeout) as publish_client:
            publish_client.publish(subject, payload=json.dumps(request, cls=ObjectEncoder))

        t.join()
        if len(result) == 0:
            resp = BridgeResponse()
            resp.Id = request.Id
            resp.IsError = True
            resp.Error = 'Нет отвера от сервера'
            result.append(resp.__dict__)
        return result[0]

    @staticmethod
    def _get_subscription_subject(subject: str, request_id: str) -> str:
        return f'{subject}.{request_id}'
