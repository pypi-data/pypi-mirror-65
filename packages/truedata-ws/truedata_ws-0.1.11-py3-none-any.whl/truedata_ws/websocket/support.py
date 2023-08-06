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

    def __eq__(self, other):
        res = True
        try:
            if self.timestamp != other.timestamp \
                    or self.symbol != other.symbol\
                    or self.ltp != other.ltp\
                    or self.best_bid_price != other.best_bid_price\
                    or self.best_bid_qty != other.best_bid_qty\
                    or self.best_ask_price != other.best_ask_price\
                    or self.best_ask_qty != other.best_ask_qty\
                    or self.volume != other.volume\
                    or self.atp != other.atp\
                    or self.oi != other.oi\
                    or self.turnover != other.turnover:
                res = False
        except AttributeError:
            res = False
        return res


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
