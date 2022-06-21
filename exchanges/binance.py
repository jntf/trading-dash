from binance.client import Client
import pandas as pd
from datetime import datetime

class Binance:
    
    def __init__(self):
        self.client = Client()
        self.time = {
                        '60' : '1m',
                        '180' : '3m',
                        '300' : '5m',
                        '900' : '15m',
                        '1800' : '30m',
                        '3600' : '1h',
                        '7200' : '2h',
                        '14400' : '4h',
                        '21600' : '6h',
                        '28800' : '8h',
                        '43200' : '12h',
                        '86400' : '1d',
                        '259200' : '3d',
                        # 'KLINE_INTERVAL_1WEEK' : '1w',
                        # 'KLINE_INTERVAL_1MONTH' : '1M',
                    }
        self.periods = [50, 100, 150, 250, 325, 500]
        
    def get_pairs_usdt(self):
        self.prices = self.client.get_all_tickers()
        return {list(i.values())[0]: list(i.values())[1] for i in self.prices if list(i.values())[0].endswith("USDT")}
    
    def get_df_token(self, value, rangetime):
        self.candles = self.client.get_klines(symbol=value, interval=rangetime)
        df_token = pd.DataFrame(self.candles, columns = ['time', 'open', 'high', 'low', 'close', 'volume', 'close_time', 'quote_av', 'trades', 'tb_base', 'tb_quote', 'cbi'])
        df_token = df_token[['time', 'open', 'high', 'low', 'close']]
        df_token.time = df_token.time.apply(lambda x: datetime.fromtimestamp(x/1000))
        return df_token