from enum import Enum

SYMBOL='symbol'
PERIOD='period'
MULT='mult'
CHANGEATR='changeATR'
CORENAME='name'
HAOPTION='haoption'
MARGIN='margin'
WRITER='writer'

NAMEKEY = 'name'
PACKAGE = 'sj_trading.Strategy'

CFG_PATH_STRATEGY = 'src/config/strategy'
CFG_PATH_ORDER = 'src/config/order'
CFG_PATH_BACKTEST = 'src/config/backtest'

MAIN_PATH_STRATEGY = 'src/sj_trading/Strategy'

EXIT_FILE = 'exit'

EXIT_DEFAULT = 'default'
EXIT_ATR = 'atr'
EXIT_TICK = 'tick'

class PositionType(int ,Enum):
    LONG = 1
    SHORT = -1
    EMPTY = 0

class OrderClassType(int, Enum):
    TRADE = 1
    RESPONSE_ORDER = 2   # 委託回報
    RESPONSE_DEAL = 3    # 成交回報