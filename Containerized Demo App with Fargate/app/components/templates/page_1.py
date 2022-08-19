from dash import dcc
from dash import html
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
from components.callbacks import callback_1

### dropdown
dropdown_1 = dcc.Dropdown(
    id='xaxis-column',
    style={'width': '48%', 'display': 'inline-block'})
            
dropdown_2 = dcc.Dropdown(
    id='yaxis-column',
    style={'width': '48%', 'display': 'inline-block'})
    
### scatter plot
scatter_plot = dcc.Graph(id='indicator-graphic')

### final layout ###
layout = html.Div(
    children=[
        dropdown_1,
        dropdown_2,
        scatter_plot
    ]
)