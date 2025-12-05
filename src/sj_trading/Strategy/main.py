import threading
from .BaseStrategy import BaseStrategy
from sj_trading.Quote.Publisher import QuotePublisher
from sj_trading.Utils.log import system_logger

# 先用一條thread統一管理所有strategies
def run_strategy(
    end_event: threading.Event,
    pause_event: threading.Event,
    strategies: list[BaseStrategy],
    publisher: QuotePublisher,
):
    system_logger.info(f'Strategy thread start with id: {threading.get_native_id()}')
    for strategy in strategies:
        if strategy.quote_sub_id == -1:
            strategy.quote_sub_id = publisher.add_subscriber(strategy)
    
    while not end_event.is_set():
        publisher.notify_all(pause_event.is_set())