class LiveData:
    def __init__(self, symbol):
        self.timestamp = None
        self.exchange = None
        self.symbol = symbol
        self.symbol_id = None
        self.ltp = None
        self.best_bid_price = None
        self.best_bid_qty = None
        self.best_ask_price = None
        self.best_ask_qty = None
        self.volume = None
        self.atp = None
        self.oi = None
        self.turnover = None
        self.bids = []
        self.asks = []


class TouchlineData:
    def __init__(self):
        self.symbol = None
        self.truedata_id = None
        self.raw_data = None
        self.open = None
        self.high = None
        self.low = None
        self.close = None
        self.prev_close = None
