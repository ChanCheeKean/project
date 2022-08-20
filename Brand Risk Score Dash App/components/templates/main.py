import dash_html_components as html
import dash_bootstrap_components as dbc
import dash_core_components as dcc
from components.callbacks import main_cb
from datetime import datetime, timedelta
import pandas as pd
import numpy as np
from utils.data_loader import fetch_data

#############
### Clock ###
#############
clock = html.Div([
        html.Span('Edelman Trust Stream', className='text-black font-weight-bold h6'),
        html.Sub('ver0.1.5', className='font-italic'),
        html.Span(' | ', className='text-black lead'),
        html.Span(id="current_date", className='text-black-50'),
        html.Span('  ', className='text-white'),
        html.Span(id = "current_time", className='text-black-50'),
        html.Span(' | ', className= 'text-black lead'),
        dbc.Button(html.Img(src = './static/refresh-icon.png', className='icon'), 
                   className='d-inline-block icon-button', 
                   outline=False),
        ], className='time float-right pr-3')

#############
### Clock ###
#############
logo = html.Div([
    clock,
    html.Img(src='./static/dxi-logo.png', className='logo')
    ], className='top_bar')

###############
### Content ###
###############
# triggered by callback
content = html.Div(id='page_content')

###########
### Tab ###
###########
tabs = dbc.Tabs([
    dbc.Tab(label="OVERVIEW", tab_id='main_tab_a'),
    dbc.Tab(label="ANALYSIS", tab_id='main_tab_b'),
    dbc.Tab(label="ARCHIVE", tab_id='main_tab_c'),
    dbc.Tab(label="COMING SOON...", tab_id='main_tab_d', disabled=True),
    ] , 
    id='main_tab',
    active_tab="main_tab_a",
    )

############
### Data ###
############
index_mapping = pd.read_csv('./data/index_term_category.csv')

########################
### Combining Layout ###
########################
layout = html.Div([
        dcc.Interval(id='clock_interval_30', interval=30*1000, n_intervals=0),
        dcc.Interval(id='clock_interval_5', interval=5*1000, n_intervals=0),
        html.Div(id='pg2_intermediate_map',  className='d-none', children=index_mapping.to_json()),
        # html.Div(id='pg2_intermediate_real',  className='d-none', children=d2.to_json()),
        logo,
        tabs,
        content
        ])
