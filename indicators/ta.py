import pandas as pd
import plotly.graph_objects as go
import ta
from ta.volatility import BollingerBands


class Ta_indicators:
    
    def __init__(self, df, period):
        self.df = df
        self.p = period
        
    # Moyenne Mobile
    def ema7(self):
        self.df['ema'] = ta.trend.ema_indicator(close=self.df['close'], window=7)
        graph = go.Scatter(name='EMA 7',x=self.df[self.p:].time,y=self.df[self.p:].ema, )
        return graph
    def ema20(self):
        self.df['ema'] = ta.trend.ema_indicator(close=self.df['close'], window=20)
        graph = go.Scatter(name='EMA 20',x=self.df[self.p:].time,y=self.df[self.p:].ema, )
        return graph
    def ema48(self):
        self.df['ema'] = ta.trend.ema_indicator(close=self.df['close'], window=48)
        graph = go.Scatter(name='EMA 48',x=self.df[self.p:].time,y=self.df[self.p:].ema, )
        return graph
    def ema100(self):
        self.df['ema'] = ta.trend.ema_indicator(close=self.df['close'], window=100)
        graph = go.Scatter(name='EMA 100',x=self.df[self.p:].time,y=self.df[self.p:].ema, )
        return graph
    def ema200(self):
        self.df['ema'] = ta.trend.ema_indicator(close=self.df['close'], window=200)
        graph = go.Scatter(name='EMA 200',x=self.df[self.p:].time,y=self.df[self.p:].ema, )
        return graph
    
    # Bands de Bollinger
    def bbh(self):
        indicatorbb = BollingerBands(close=self.df.close, window=20, window_dev=2)
        self.df["bbh"] = indicatorbb.bollinger_hband()
        graph = go.Scatter(name='BBH', mode = 'lines', x = self.df[self.p:].time, y = self.df[self.p:].bbh, marker=dict( color='LightSkyBlue', ))
        return graph
    def bbl(self):
        indicatorbb = BollingerBands(close=self.df.close, window=20, window_dev=2)
        self.df["bbl"] = indicatorbb.bollinger_lband()
        graph = go.Scatter(name='BBL', mode = 'lines', x = self.df[self.p:].time, y = self.df[self.p:].bbl, marker=dict( color='LightSkyBlue', ))
        return graph
    def bbm(self):
        indicatorbb = BollingerBands(close=self.df.close, window=20, window_dev=2)
        self.df["bbm"] = indicatorbb.bollinger_mavg()
        graph = go.Scatter(name='BBL', mode = 'lines', x = self.df[self.p:].time, y = self.df[self.p:].bbm, marker=dict( color='LightSkyBlue', ))
        return graph