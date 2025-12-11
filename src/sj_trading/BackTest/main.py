import shioaji as sj
import backtrader as bt
import time
import threading
import logging
import sys
import io
import csv
import pandas as pd
from sj_trading.Strategy import *
from sj_trading.Utils.Contract import ContractResolver
from sj_trading.Utils import Kbar
from sj_trading.Utils.log import system_logger, backtest_logger
from sj_trading.Strategy.RangeFilter_1 import RangeFilter_1_bt
from sj_trading.Strategy.RangeFilter_2 import RangeFilter_2_bt
from sj_trading.Utils.Futures import *
from .Observer import CashValueObserver

START='start'
END='end'
SYMBOL='symbol'
INTERVAL='interval'
TYPE='type'
STRATEGY='strategy'
FUND='fund'
COMMISSION='commission'

bt_strategies_cls = {
    'RangeFilter_1': RangeFilter_1_bt,
    'RangeFilter_2': RangeFilter_2_bt,
}

bt_dfcfg = {
    START: '2025-11-01',
    END: '2025-11-22',
    SYMBOL: 'MXF',
    INTERVAL: '15T',
    TYPE: 'kbars',
    STRATEGY: 'RangeFilter_1',
    FUND: 100000,
    COMMISSION: 0.001,
}

def output_stat(cfg: dict, stat, cerebro):
    ret = stat.analyzers.returns.get_analysis()
    sharpe = stat.analyzers.sharpe.get_analysis()
    dd = stat.analyzers.drawdown.get_analysis()
    trades = stat.analyzers.trades.get_analysis()

    total_trades = trades.total.total if trades.total.total else 0
    win_rate = (trades.won.total / total_trades * 100) if total_trades > 0 else 0

    stats_items = {
        'Total Return (%)':      f'{ret.get('rtot', 0) * 100:,.2f}',
        'Annual Return (%)':     f'{ret.get('rnorm', 0) * 100:,.2f}',
        'Sharpe Ratio':          sharpe.get('sharperatio', None),
        'Max Drawdown (%)':      f'{dd.max.drawdown:,.2f}',
        'Max Drawdown Duration': dd.max.len,
        'Total Trades':          total_trades,
        'Win Rate (%)':          f'{win_rate:,.2f}',
        'End fund:':             f'{cerebro.broker.getvalue():,.2f}',
    }

    key_width_cfg = max(len(k) for k in cfg.keys()) if cfg else 10
    key_width_stats = max(len(k) for k in stats_items.keys())

    # 外框長度
    table_width = max(key_width_cfg, key_width_stats) + 30

    report = []
    border = '=' * table_width

    report.append(border)
    report.append('               Backtest Report               '.center(table_width))
    report.append(border)

    report.append('Config')
    for k, v in cfg.items():
        report.append(f'{k.ljust(key_width_cfg)} : {v}')

    report.append('\nStatistics')
    for k, v in stats_items.items():
        report.append(f'{k.ljust(key_width_stats)} : {v}')

    report.append(border)

    return '\n'.join(report)

def run_backtest(
    api: sj.Shioaji,
    cfg: dict,
    resolver: ContractResolver, 
    st_cfg: list[dict],
):
    if not cfg:
        backtest_logger.error('Fail to run backtest: please check src/config/backtest')
        return
    
        
    bt_start = cfg.get(START, bt_dfcfg[START])
    bt_end = cfg.get(END, bt_dfcfg[END])
    bt_symbol = cfg.get(SYMBOL, bt_dfcfg[SYMBOL])
    bt_commission = cfg.get(COMMISSION, bt_dfcfg[COMMISSION])
    bt_fund = cfg.get(FUND, bt_dfcfg[FUND])
    bt_interval = cfg.get(INTERVAL, bt_dfcfg[INTERVAL])
    bt_strategy = cfg.get(STRATEGY, bt_dfcfg[STRATEGY])
    
    csvfile = open("backtest_output.csv", "w", newline='')
    fieldnames = [
        'type', 'bar_dt', 'open', 'high', 'low', 'close', 'volume',
        'order_ref', 'order_action', 'price', 'size', 'value', 'commission',
        'exec_dt',
        'gross_profit', 'net_profit', 'open_dt', 'close_dt'
    ]
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    st_cfg[bt_strategy]['writer'] = writer
    
    backtest_logger.info('New backtest request')
    if cfg.get(TYPE, bt_dfcfg[TYPE]) == 'kbars':
        contract = resolver.resolve(bt_symbol)
        bt_input = api.kbars(
            contract=contract,
            start=bt_start,
            end=bt_end,
        )

    bt_input = pd.DataFrame({**bt_input})
    bt_input.ts = pd.to_datetime(bt_input.ts)
    bt_input = bt_input.set_index('ts')
    bt_input = Kbar.resample(bt_input, bt_interval)
    
    data = bt.feeds.PandasData(
        dataname=bt_input,
        timeframe=bt.TimeFrame.Minutes,
    )

    cerebro = bt.Cerebro()
    cerebro.adddata(data)
    
    cerebro.addanalyzer(bt.analyzers.SharpeRatio, _name='sharpe')
    cerebro.addanalyzer(bt.analyzers.DrawDown, _name='drawdown')
    cerebro.addanalyzer(bt.analyzers.Returns, _name='returns')
    cerebro.addanalyzer(bt.analyzers.TradeAnalyzer, _name='trades')
    cerebro.addanalyzer(bt.analyzers.AnnualReturn, _name='annual')
    
    cerebro.addstrategy(
        bt_strategies_cls[bt_strategy],
        **st_cfg[bt_strategy],
    )

    cerebro.addobserver(CashValueObserver)
    cerebro.broker.setcash(bt_fund)

    cerebro.broker.setcommission(
        commission=bt_commission,  # Future commission為固定值 * size
        margin=ft_margin_orig[bt_symbol],  # Future須設定margin
        mult=ft_mult[bt_symbol],  
    )
    
    bt_cfg = {
        START: bt_start,
        END: bt_end,
        SYMBOL: bt_symbol,
        INTERVAL: bt_interval,
        STRATEGY: bt_strategy,
        FUND: bt_fund,
        COMMISSION: bt_commission,
    }
    backtest_logger.info(f'Start backtesting, config: {bt_cfg}')
    res = cerebro.run()  # res: list (# of strategies)
    fig = cerebro.plot(
        style='candlestick',
        iplot=False,
        savefig=True,
        figscale=2.5,   # 放大整張圖
        width=25,
        height=9,
    )[0][0]

    fig.savefig(f'bt_test.png', bbox_inches='tight')
    log_stat = output_stat(cfg, res[0], cerebro)
    backtest_logger.info('\n' + log_stat)
    
    csvfile.close()

    