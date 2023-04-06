from dash import html
import dash_bootstrap_components as dbc

### video streaming ###
video_container = html.Div(
    html.Img(src="/video_feed"),
    className='mt-4',
    )

### main layout ###
layout = html.Div([
    dbc.Row([
            dbc.Col(html.Div(), width=4),
            dbc.Col(video_container, width=4),
            dbc.Col(html.Div(), width=4),
            ]), 
    ])