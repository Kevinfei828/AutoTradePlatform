#　設定檔
1. 分為回測 (backtest), 下單 (order), 策略 (strategy)，放在src/config下
2. 設定方式
    1. 格式: 參數種類=參數值，已提供回測和下單設定檔範本在各自的test.cfg
    2. 一定要先設定好策略設定檔，檔名為{策略名}.cfg，後續回測和下單功能都會抓這邊的檔案
    3. 回測和下單用strategy={策略名}調整使用策略，下單可設定strategy=All，代表此下單設定檔適用所有策略，注意策略設定檔名和回測/下單設定的策略名需一致
    4. 同一strategy可設定多種order cfg
3. 添加新策略
    1. src/config/strategy添加.cfg
    2. src/sj_trading/Strategy添加策略.py
    3. python class name和.cfg file name需一致
    4. __init__參數和.cfg參數名需一致 (順序可不一)