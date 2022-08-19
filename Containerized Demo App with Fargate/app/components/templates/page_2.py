from dash import dcc
from dash import html
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px

### text input and output ###
text_container = html.Div(
    dbc.Container(
        [
            html.H1("Sentiment-Analyser", className="fw-bolder"),
            html.P("Enter Text to get the Sentiment in return"),
            html.Hr(className="my-3"),
            
            # text input area
            dbc.Textarea(id="input", placeholder="Type something..."),
            dbc.Button("Compute", id="submit-button", className="my-2"),
            html.Br(),
            
            # text ouput
            dbc.Alert(
                id="output", 
                children=["This is a primary alert"], style={"visibility" : 'hidden'}),
            
        ],
        fluid=True,
        className="py-3",
    ),
    className="p-3 bg-light rounded-3",
)

### final layout ###
layout = html.Div(
    children=[
        text_container,  
    ]
)
    




    