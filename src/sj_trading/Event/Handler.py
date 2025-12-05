import threading
import time

'''
https://sinotrade.github.io/zh/tutor/callback/event_cb/
'''

class EventHandler:
    def __init__(self, api):
        self.api = api
        self.quote_event = threading.Event()
        
        # 註冊事件
        self.api.quote.set_event_callback(self.event_callback)

    def event_callback(self, resp_code: int, event_code: int, info: str, event: str):
        print(f"Event code: {event_code} | Event: {event} | info: {info}")

        if event_code == 16 and resp_code == 200:
            time.sleep(0.5)
            self.quote_event.set()
        
        