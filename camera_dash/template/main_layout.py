from dash import html
import dash_bootstrap_components as dbc

### video streaming ###
video_container = html.Div(
    html.Img(src="/video_feed", style={'width' : '450px', 'height': '800px'}),
    className='mt-4',
    )

### main layout ###
layout = html.Div([
    dbc.Row([
            dbc.Col(video_container, width=2),
            dbc.Col(html.Div(), width=5),
            dbc.Col(html.Div(), width=5),
            ]), 
    ])