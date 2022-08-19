import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import weather_widget as wio
from utils.dash_helpers import parse_options
import dash_daq as daq
import pandas as pd

##################
# Weather Forecast Widget
##################
card_weather = dbc.Card([
                            dbc.CardHeader('Schwäbisch Gmünd 7-Days Weather Forecast', className = 'card_header'),
                            html.Div(
                                wio.WeatherWidget(
                                    id = "weatherio",
                                    location='schwabisch-gmund'
                                )
                            )
                        ],
                        className = 'card')

##################
# tsplot
##################
bottom_bar = html.Div([dcc.Tabs([
                                dcc.Tab(label = 'Hourly', className = 'bot_tab_item', selected_className='bot_tab_activated', value='hour'),
                                dcc.Tab(label = 'Daily', className = 'bot_tab_item', selected_className='bot_tab_activated', value='day'),
                                dcc.Tab(label = 'Monthly', className = 'bot_tab_item', selected_className='bot_tab_activated', value='month'),
                                ], className = 'bot_tab_nav', id="env_tabs", value='hour'),
                ])

card_tsplot = dbc.Card(
        [
                dbc.CardHeader('Air Quality (NO2) Forecast', className = 'card_header'),
                html.Div(bottom_bar, ),
                dcc.Loading(
                    children = html.Div(dcc.Graph(id='env_tsplot', style= dict(height = '210px'))),
                    type="default"),
        ],className = 'card')

##################
# Gauge
##################
# layout components
NO_gauge = daq.Gauge(  color={"gradient":True,"ranges":{"green":[0,90],"gold":[90,150],"red":[150,200]}},
                            label='NO2', showCurrentValue=True, units = 'ug/m3',
                            scale={'start': 0, 'interval': 25,}, size = 150,
                            value=100, max=200, min=0, id = 'NO_gauge',labelPosition = 'top',
                            style=dict(display = 'inline-block'), className = 'pt-1 gauge',)

PM10_gauge = daq.Gauge(     color={"gradient":True,"ranges":{"green":[0,50],"gold":[50,80],"red":[80,150]}},
                            label='PM10', showCurrentValue=True, units = 'ug/m3',
                            scale={'start': 0, 'interval': 25,}, size = 150,
                            value=50, max=150, min=0, id = 'PM10_gauge',labelPosition = 'top',
                            style=dict(display = 'inline-block'), className = 'pt-1 gauge',)

PM25_gauge = daq.Gauge(   color={"gradient":True,"ranges":{"green":[0,50],"gold":[50,80],"red":[80,150]}},
                            label='PM2.5', showCurrentValue=True, units = 'ug/m3',
                            scale={'start': 0, 'interval': 25,}, size = 150,
                            value=90, max=150, min=0, id = 'PM25_gauge',labelPosition = 'top',
                            style=dict(display = 'inline-block'), className = 'pt-1 gauge',)

status = html.Div([
        html.Span('Air Quality: ', className = 'font-weight-bold text-white d-inline-block pl-2'),
        html.Span('Below Average', className = 'font-weight-bold text-warning d-line-block pl-3'),
        ])

card_gauge = dbc.Card([
        dbc.CardHeader('Air Quality Metering', className = 'card_header'),
        dbc.Row([
                dbc.Col(NO_gauge, width = 4),
                dbc.Col(PM10_gauge, width = 4),
                dbc.Col(PM25_gauge, width = 4),
                ], ),
        status
        ], className = 'card')


##################
# Wind Direction
##################

card_wind = dbc.Card([
        dbc.CardHeader('Wind Direction', className = 'card_header'),
        html.Div(dcc.Graph(id='wind_polar', style= dict(height = '225px'))),
        ], className = 'card')

##################
# Main Layout
##################
layout = html.Div([
        dbc.Row([
                dbc.Col(card_weather,width = 4),
                dbc.Col(card_tsplot, width = 8),
                ], className = 'my-2'),

        dbc.Row([
                dbc.Col(card_gauge, width = 8),
                dbc.Col(card_wind, width = 4),
                ], className = 'my-2'),

        dcc.Interval(id='env_interval', interval = 5*1000, n_intervals=0),
        html.Div(id='env_intermediate',  className = 'd-none', children = pd.DataFrame().to_json()),
        ])