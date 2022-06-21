import pandas as pd
from datetime import datetime
import requests

class Ftx:
    
    def __init__(self):
        self.ftx = requests
        self.endpoint_url = 'https://ftx.com/api/markets'
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
        
    def get_pairs_usd(self):
        self.prices = self.ftx.get(self.endpoint_url).json()['result']
        return {i['name']: i['price'] for i in self.prices if (i['name'].endswith('USD') or i['name'].endswith('USDT')) and isinstance(i['price'], float)}
    
    def get_df_token(self, value, rangetime):
        time_dict = {j: i for i, j in self.time.items()}
        historical = requests.get(f'https://ftx.com/api/markets/{value}/candles?resolution={time_dict[rangetime]}&start_time=1512082800').json()
        df_token = pd.DataFrame(historical['result'])
        df_token = df_token[['time', 'open', 'high', 'low', 'close']]
        df_token.time = df_token.time.apply(lambda x: datetime.fromtimestamp(x/1000))
        return df_token[-500:]