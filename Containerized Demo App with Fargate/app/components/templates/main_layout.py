import pandas as pd
import numpy as np
from app import app
from dash import dcc
from dash import html
import dash_bootstrap_components as dbc
from components.callbacks import main_callback

### tabs for page selection ###
tabs = dbc.Tabs([
            dbc.Tab(label="Page A", tab_id='main_tab_a'),
            dbc.Tab(label="Page B", tab_id='main_tab_b')], 
        id='main_tab',
        active_tab="main_tab_a",
    )

### content to be display ###
content = html.Div(id='page_content', className='content')

### final layout ###
layout = html.Div([
        dcc.Location(id="url"),
        tabs,
        content
    ])