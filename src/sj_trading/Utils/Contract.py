class ContractResolver:
    """
    自動從永豐 API 讀取所有商品分類，
    並提供 symbol -> API contract 查詢。
    """
    def __init__(self, api):
        self.api = api
        self.mapping = {}  # symbol -> (category_name, api_contract)

        self._load_category("Indexs")
        self._load_category("Stocks")
        self._load_category("Futures")
        self._load_category("Options")

    def _load_category(self, category_name: str):
        """
        讀取 api.Contracts.<Category> 底下所有商品。
        例如 api.Contracts.Futures.MXF
        """
        category_obj = getattr(self.api.Contracts, category_name)
        
        for attr in dir(category_obj):
            if attr.startswith("_"):
                continue  # 跳過內建屬性

            try:
                contract = getattr(category_obj, attr)
            except Exception:
                continue  # 非商品就跳過

            # e.g. {"MXF": ("Futures", <contract>)}
            self.mapping[attr] = (category_name, contract)

    def resolve(self, symbol: str):
        """
        給定「商品代碼字串」，回傳永豐 API contract 物件。
        例如 resolve("MXF") -> api.Contracts.Futures.MXF
        """
        if symbol not in self.mapping:
            raise ValueError(f"Unknown symbol: {symbol}")

        _, contract = self.mapping[symbol]
        return contract

    def get_type(self, symbol: str) -> str:
        """
        給定「商品代碼字串」，回傳類別：
        Indexs / Stocks / Futures / Options
        """
        if symbol not in self.mapping:
            raise ValueError(f"Unknown symbol: {symbol}")

        category, _ = self.mapping[symbol]
        return category