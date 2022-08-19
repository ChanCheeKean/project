import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import weather_widget as wio
from utils.dash_helpers import parse_options
import dash_daq as daq
import pandas as pd

##################
# Tsplot
##################
bottom_bar = html.Div([dcc.Tabs([
                                dcc.Tab(label = 'Hourly', className = 'bot_tab_item', selected_className='bot_tab_activated', value='hour'),
                                dcc.Tab(label = 'Daily', className = 'bot_tab_item', selected_className='bot_tab_activated', value='day'),
                                dcc.Tab(label = 'Monthly', className = 'bot_tab_item', selected_className='bot_tab_activated', value='month'),
                                ], className = 'bot_tab_nav', id="da_tabs", value='hour'),
                ])

card_tsplot = dbc.Card(
        [
                dbc.CardHeader('1-year Historical Data', className = 'card_header'),
                html.Div(bottom_bar, ),
                dcc.Loading(
                    children = html.Div(dcc.Graph(id='da_avg_tsplot', style= dict(height = '400px'))),
                    type="default"),
        ],className = 'card')
                
                
##################
# Correlation Plot
##################
card_corr = dbc.Card(
        [
                dbc.CardHeader('Correlation Heatmap', className = 'card_header'),
                dcc.Loading(
                    children = html.Div(dcc.Graph(id='da_corr_hm', style= dict(height = '440px'))),
                    type="default"),
        ],className = 'card')        

                
##################
# Main Layout
##################
layout = html.Div([

        dbc.Row([
                dbc.Col(card_tsplot, width = 6),
                dbc.Col(card_corr, width = 6),
                ], className = 'my-2'),

#        dcc.Interval(id='da_interval', interval = 5*1000, n_intervals=0),
        html.Div(id='da_intermediate',  className = 'd-none', children = pd.DataFrame().to_json()),
        ])
