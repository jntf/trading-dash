from dash import Dash, dcc, html, Input, Output, State
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import pandas as pd
import numpy as np
from exchanges.binance import Binance
from exchanges.ftx import Ftx
from indicators.ta import Ta_indicators

# Binance
# client = Binance().client
binance = Binance()
usdt_dict = binance.get_pairs_usdt()

# FTX
ftx = Ftx()
usdt_dict.update(ftx.get_pairs_usd())

periods = [50, 100, 150, 250, 325, 500]
select_time = ['1m', '3m', '5m', '15m', '30m', '1h', '2h', '4h', '6h', '8h', '12h', '1d', '3d']
exchanges = ['Binance', 'FTX']

# Indicator
indicators = {
    'ema7': 'EMA = Moyenne mobile 7', 
    'ema20': 'EMA = Moyenne mobile 20', 
    'ema48': 'EMA = Moyenne mobile 48', 
    'ema100': 'EMA = Moyenne mobile 100', 
    'ema200': 'EMA = Moyenne mobile 200', 
    'bb': 'Bandes de Bollinger'
}


app = Dash(external_stylesheets=[dbc.themes.FLATLY])


app.layout = html.Div([
    dbc.Container([
        dbc.Row([
            dbc.Row([
                dbc.Col([
                    dbc.Card([
                        html.Div([
                            html.H4('{} CHART'.format('BINANCE'), className="pb-2"),                    
                        ], className='text-center pt-3'),
                    ], className='bg-white col-4 mx-auto shadow', style={'border-radius':'1em', 'text-align': 'center', 'box-shadow': '0 5px 10px rgba(0,0,0,.2)'})
                ], width=12)
            ], className='pt-4 pb-5'),
            dbc.Col([
                dcc.Interval(
                    id="interval-component",
                    interval=3000,
                    n_intervals=0,
                ),
                dbc.Row([
                    dbc.Col([
                        html.Div([
                            html.Div([
                                dcc.Dropdown(
                                    options = [
                                        {
                                            'label': i,
                                            'value': i
                                         } for i in exchanges
                                    ],
                                    value= 'Binance',
                                    clearable = False,
                                    id = 'exchanges'
                                ),
                            ], className='mx-auto')
                        ], className=''),
                    ], class_name='pb-1', width=2),
                    dbc.Col([
                        html.Div([
                            html.Div([
                                dcc.Dropdown(
                                    options = [
                                        {
                                            'label': 'Interval: ' + str(i),
                                            'value': i
                                        } for i in select_time
                                    ],
                                    value='1h',
                                    clearable = False,
                                    id = 'time'
                                ),
                            ], className='mx-auto')
                        ], className=''),
                    ], class_name='pb-1', width=2),
                    dbc.Col([
                        html.Div([
                            html.Div([
                                dcc.Dropdown(
                                    options = [
                                        {
                                            'label': 'Period: ' + str(i),
                                            'value': i
                                         } for i in periods
                                    ],
                                    value= 100,
                                    clearable = False,
                                    id = 'period'
                                ),
                            ], className='mx-auto')
                        ], className=''),
                    ], class_name='pb-1', width=2),
                    dbc.Col([
                        dcc.Checklist(
                            id='toggle-rangeslider',
                            options=[{'label': '  Include Rangeslider', 
                                    'value': 'slider'}],
                            value=[]
                        ),
                    ], class_name='pt-1', width=3 ),
                ]),
                dbc.Card([
                    dcc.Graph(id="candles_chart", config={'displayModeBar': False}, style={'width': '100%', 'height': '80vh'}),
                ], className='shadow', style={'border-radius':'2em', 'text-align': 'center', 'box-shadow': '0 5px 10px rgba(0,0,0,.2)'}),
            ], width=9), 
            dbc.Col([
                dbc.Card([
                    dbc.Col([
                            html.Div([
                                html.Div([
                                    html.P('Crypto', className='col-11 text-center pt-1'),
                                ], className=''),
                                html.Div([
                                    dcc.Dropdown(
                                        options = [
                                            {
                                                'label': i + ' : $' + str(round(float(j), 2)), 
                                                'value' : i
                                            } for i, j in usdt_dict.items()
                                        ], 
                                        value = 'BTCUSDT',
                                        clearable = False,
                                        id = "dropdown",
                                    ),
                                ], className="mx-auto"),
                            ], className='p-2'),
                        ], class_name='mx-auto', width=11),
                        dbc.Col([
                            html.Div([
                                html.P('Select Indicator', className='col-11 text-center pt-1')
                            ]),
                            html.Div([
                                dcc.Dropdown(
                                    options = [
                                        {
                                            'label': j, 
                                            'value': i
                                        } for i, j in indicators.items()
                                    ],
                                    value = '', 
                                    multi = True,
                                    id = 'indicator'
                                )
                            ], className='')
                        ], class_name='mb-3')
                ], className='shadow p-3', style={'border-radius':'2em', 'text-align': 'center', 'box-shadow': '0 5px 10px rgba(0,0,0,.2)'}),
            ], class_name='mt-5', width=3)
        ]),
        # dbc.Card([
        #     dcc.Graph(id="bubbles", config={'displayModeBar': False}, style={'width': '100%', 'height': '80vh'}),
        #     # dcc.Interval(
        #     #     id="interval-bubble",
        #     #     interval=3000,
        #     #     n_intervals=0,
        #     # ),
        # ], className='shadow', style={'border-radius':'2em', 'text-align': 'center', 'box-shadow': '0 5px 10px rgba(0,0,0,.2)'})
    ]), 
])

@app.callback(
    Output("candles_chart", "figure"), 
    Input("dropdown", "value"),
    Input("time", "value"),
    Input("toggle-rangeslider", "value"),
    Input("period", "value"),
    Input("indicator", "value"), 
    Input(component_id = 'interval-component', component_property = 'n_intervals')
)

def display_candlestick(value, rangetime, ranges, p, indicator, refresh):
    
    pair = value
    
    # Get df
    if '/' in value:
        df_token = ftx.get_df_token(value, rangetime)
    else:
        df_token = binance.get_df_token(value, rangetime)
    # Period
    p = 500 - p
    # Indicator
    ta_indic = Ta_indicators(df_token, p)
    
    fig = go.Figure()
    
    fig.add_trace(
        go.Candlestick(
            name='',
            x=df_token[p:].time,
            open=df_token[p:].open,
            high=df_token[p:].high,
            low=df_token[p:].low,
            close=df_token[p:].close
        )
    )
    
    if indicator:
        if 'ema7' in indicator:
            fig.add_trace(ta_indic.ema7())
        if 'ema20' in indicator:
            fig.add_trace(ta_indic.ema20())
        if 'ema48' in indicator:
            fig.add_trace(ta_indic.ema48())
        if 'ema100' in indicator:
            fig.add_trace(ta_indic.ema100())
        if 'ema200' in indicator:
            fig.add_trace(ta_indic.ema200())
        if 'bb' in indicator:
            fig.add_trace(ta_indic.bbh())
            fig.add_trace(ta_indic.bbl())
            fig.add_trace(ta_indic.bbm())
    
    fig.update_layout(
        barmode='stack', 
        title={
            'text': "<b class='text-white'>Trading View</b>", 
            'x': .10, 
            'y': .95
        }, 
        legend={
            'x': 0,
            'y': 0,
            'bordercolor': 'white', 
            'borderwidth': 2,
            'bgcolor': 'white',
        }, 
        plot_bgcolor='rgba(0, 0, 0, 0)',
        paper_bgcolor='rgba(0, 0, 0, 0)',
        xaxis_showgrid=False,
        yaxis_showgrid=False,
        
        xaxis_rangeslider_visible = 'slider' in ranges,
    ), 
    # fig.update_yaxes(
    #     range= [
    #         float(df_token[350:].low.min()) * 0.99, 
    #         float(df_token[350:].high.max()) * 1.01
    #     ]
    # )
    
    return fig
    

if __name__ == "__main__":
    app.run_server(debug=True)
