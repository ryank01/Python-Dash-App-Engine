#-*- coding: utf-8 -*-
import os
import dash
import dash_core_components as dcc
import dash_html_components as html
import requests
import pandas as pd
import plotly.graph_objs as go
from flask import Flask
from dash.dependencies import Input, Output

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server

colors = {
        'background': '#111111',
        'text': '#7FDBFF'    
    }


# fetch stock data
def fetch_data(stock_ticker='MSFT'):
    r = requests.get('https://www.alphavantage.co/query?function=TIME_SERIES_MONTHLY&symbol={}&apikey=K87BB8H31SVY3OBA'.format(stock_ticker))
    # fetch bb data
    #indicator_adx = requests.get('https://www.alphavantage.co/query?function=ADX&symbol=USDEUR&interval=monthly&time_period=10&apikey=K87BB8H31SVY3OBA')
    indicator_bb_bands = requests.get('https://www.alphavantage.co/query?function=BBANDS&symbol={}&interval=monthly&time_period=5&series_type=close&nbdevup=3&nbdevdn=3&apikey=K87BB8H31SVY3OBA'.format(stock_ticker))
    return r, indicator_bb_bands

r, indicator_bb_bands = fetch_data()

stock_data = r.json()
stock_df = pd.DataFrame.from_dict(stock_data['Monthly Time Series'])


#adx_data = indicator_adx.json()
#adx_df = pd.DataFrame.from_dict(adx_data['Technical Analysis: ADX'])

bb_data = indicator_bb_bands.json()
bb_df = pd.DataFrame.from_dict(bb_data['Technical Analysis: BBANDS'])


monthly_data_df = pd.DataFrame(index=range(0,len(stock_df.iloc[1].index)),columns=['Time', 'Open', 'High', 'Low', 'Close'])

time = stock_df.iloc[1].index # time series
open_price = [] # initialize list for open prices
#adx_values = [] # initialize list for adx values
upper_band = []
middle_band = []
lower_band = []

for price in range(len(stock_df.iloc[1])):
    open_price.append(stock_df.iloc[1][price])

#for value in range(len(adx_df.iloc[0])):
    #adx_values.append(adx_df.iloc[0][value])

for upper_value in range(len(bb_df.iloc[0])):
    upper_band.append(bb_df.iloc[0][upper_value])

for middle_value in range(len(bb_df.iloc[1])):
    middle_band.append(bb_df.iloc[1][middle_value])

for lower_value in range(len(bb_df.iloc[2])):
    lower_band.append(bb_df.iloc[2][lower_value])


trace_1 = go.Scatter(
            x = time,
            y = open_price,
            name = 'stock price',
            mode = 'lines',
            opacity = 0.7,
            marker = {
                'size': 15,
                'line': {'width': 0.5, 'color': 'white'}

            }

        )

trace_2 = go.Scatter(
            x = time,
            y = upper_band,
            name = 'upper band',
            mode = 'lines',
            opacity = 0.7,
            marker = {
                'size': 15,
                'line': {'width': 0.5, 'color': 'green'}
            }
        
        )

trace_3 = go.Scatter(
            x = time,
            y = middle_band,
            name = 'middle band',
            mode = 'lines',
            opacity = 0.7,
            marker = {
                'size': 15,
                'line': {'width': 0.5, 'color': 'green'}
            }
        
        )

trace_4 = go.Scatter(
            x = time,
            y = lower_band,
            name = 'lower band',
            mode = 'lines',
            opacity = 0.7,
            marker = {
                'size': 15,
                'line': {'width': 0.5, 'color': 'green'}
            }
            
        )



app.layout = html.Div(id='parent', style={'backgroundColor': colors['background']}, children=[
    html.H1(children='Bollinger Bands Graph',
            style = {
                'textAlign': 'center',
                'color': colors['text']
            }
        ),

    html.Div(children='''
        Price of stock plotted against bollinger bands.
    ''', style = {
                'textAlign': 'center',
                'color': colors['text']
    }),

    #dcc.Input(id='input', value='', type='text'),
    #html.Div(id='output-graph'),

    dcc.Graph(
        id='example-graph',
        figure={
            'data': [
                trace_1,
                trace_2,
                trace_3,
                trace_4
            ],
            'layout': {
                'title': 'Stock Volitility',
                'plot_bgcolor': colors['background'],
                'paper_bgcolor': colors['background'],
                'font': {
                    'color': colors['text']    
                }
            }
        }
    )
])


if __name__ == '__main__':
    app.run_server(debug=True)

