### 使用說明 (步驟2,3,5需開啟powershell，並在powershell內執行以下指令)
1. 在本地安裝git (可不安裝GUI)  
https://ithelp.ithome.com.tw/articles/10322227


2. 下載git  
    ```
    cd <Desktop或任一目錄>
    git clone https://github.com/Kevinfei828/AutoTradePlatform.git
    cd AutoTradePlatform
    ```

3. 建置專案環境 (安裝python和uv)  
    ```
    install.bat
    ```

4. 申請永豐API金鑰和憑證    
https://sinotrade.github.io/zh/tutor/prepare/token/
    在目前目錄 (AutoTradePlatform) 下新增.env檔案，並新增以下內容
    ```
    API_KEY=<前面申請的API Key>
    SECRET_KEY=<前面申請的Secret Key>
    CA_CERT_PATH=<前面設定的憑證路徑>
    CA_PASSWORD=<憑證密碼>
    ```

5. 將.env載入環境變數  
   ```
   uv add python-dotenv
   ```

6. 執行專案
   ```
   uv run sj_trading
   ```

### 設定檔
1. 目前本專案統一用設定檔管理下單/回測/交易等變數，設定檔統一放在src/config
2. config分為回測 (backtest), 下單 (order), 策略 (strategy)
3. 設定方式
    1. 格式: 參數種類=參數值，已提供回測和下單設定檔範本在各自的test.cfg
    2. 一定要先設定好策略設定檔，檔名為{策略名}.cfg，後續回測和下單功能都會抓這邊的檔案
    3. 回測和下單用strategy={策略名}調整使用策略，下單可設定strategy=All，代表此下單設定檔適用所有策略，注意策略設定檔名和回測/下單設定的策略名需一致
    4. 同一策略可套用多種下單設定
4. 添加新策略
    1. src/config/strategy添加{新策略}.cfg
    2. src/sj_trading/Strategy添加{新策略}.py
    3. python class name和.cfg file name需一致
    4. __init__參數和.cfg參數名需一致，順序可不一