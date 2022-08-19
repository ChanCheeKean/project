import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_daq as daq
import dash_html_components as html
import dash_table
import datetime as dt
from components.callbacks import page2_cb
from utils.dash_helpers import parse_options

########################
### Geographical Map ###
########################
trust_map = dbc.Card([
    # dbc.CardHeader('Geographical Distribution', className='card_header'),
    dcc.Loading(dcc.Graph(id='trust_map', config=dict(scrollZoom=True)), type='default'),
    ], className='card')

####################
### Density Plot ###
####################
density_plot = dbc.Card([
    # dbc.CardHeader('Density Plot', className='card_header'),
    dcc.Loading(dcc.Graph(id='density_plot'), type='default'),
    ], className='card')

######################
### Trust Score TS ###
######################
ts_trust_tab = html.Div([dcc.Tabs([
    dcc.Tab(label = 'HOURLY', className = 'h_tab_item', selected_className='h_tab_activated', value='h'),
    dcc.Tab(label = 'DAILY', className = 'h_tab_item', selected_className='h_tab_activated', value='d'),
    ], id="ts_trust_tab", value='d')])

trust_score_ts = dbc.Card([
    # dbc.CardHeader('Time Series Decomposition',className='card_header'),
    ts_trust_tab,
    dcc.Loading(dcc.Graph(id='page2_ts_trust'), type='default'),
    ], className='card')

#################
### bar chart ###
#################
count_bar = dbc.Card([
    # dbc.CardHeader('Chart A', className='card_header'),
    dcc.Loading(dcc.Graph(id='pg2_count_bar'), type="default"),
    ], className='card mt-3')

#################
### Pie Chart ###
#################
pie_tab = html.Div([dcc.Tabs([
    dcc.Tab(label = 'Ability', className = 'v_tab_item', selected_className='v_tab_activated', value='Ability'),
    dcc.Tab(label = 'Integrity', className = 'v_tab_item', selected_className='v_tab_activated', value='Integrity'),
    dcc.Tab(label = 'Dependability', className = 'v_tab_item', selected_className='v_tab_activated', value='Dependability'),
    dcc.Tab(label = 'Purpose', className = 'v_tab_item', selected_className='v_tab_activated', value='Purpose'),
    ], id="pg2_pie_tab", value='Dependability', className = 'v_tab_nav', vertical=True)])

pie_chart = dcc.Loading(dcc.Graph(id='page2_pie_chart'), type='default'),

pie_card = dbc.Card([
    # dbc.CardHeader('Chart B', className='card_header'),
    dbc.Row([
            dbc.Col(pie_tab, width=2, className='p-0'),
            dbc.Col(pie_chart, width=10, className='p-0'),
            ], className='mt-2'),
        
    ], className='card mt-3')

########################
### Combining Layout ###
########################
layout = html.Div([        
        dbc.Row([
            dbc.Col([trust_map, density_plot], width=7, className='px-2'),
            dbc.Col([trust_score_ts, count_bar, pie_card], width=5, className='px-2'),
            ], className='mt-2'),
        ],  className='hidden_scroll')