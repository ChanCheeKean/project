import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import dash_daq as daq
import pandas as pd
import bing_maps_smartcity as bms
from utils.dash_helpers import parse_options
from data.bingmaps_data import pp_echarging

#[pp['metadata']['hours'] for pp in pp_echarging]

##################
# map
##################
bing_map = dbc.Card([
            dbc.CardHeader('E-Charging Station', className = 'card_header'),
            bms.BingMaps(
                id = 'ev_map',
                zoom = 13,
                pushpins=pp_echarging 
                )
            ], className = 'card', style={'height': '350px'})


##################
# Table Station Overview
##################
table_header = [
        html.Thead(html.Tr([
                html.Th(html.P('Outlets', className = "font-weight-bold pl-4 pt-2 text-white")), 
                html.Th(html.P('Count', className = "font-weight-bold text-center pt-2 text-white")),
                html.Th(html.P('Avg. Charge Time', className = "font-weight-bold text-center pt-2 text-white")),
                html.Th(html.P('Occupancy', className = "font-weight-bold text-center pt-2 text-white")),
                html.Th(html.P('Price Trend', className = "font-weight-bold text-center pt-2 text-white")),
                ]), className = 'echarge_table_row')
]

table_body = [html.Tbody(id = 'ev_table_body')]

station_summary = dbc.Card([
                    dbc.CardHeader('EV Outlets', className = 'card_header'),
                    dcc.Loading(
                                children =  dbc.Table(table_header + table_body,  style = dict(height = '200px')),
                                type="default"),
                    ], className = 'card mt-2')

##################
# Station info
##################
station_card = dbc.Card([
                    dbc.CardHeader('Station Infomation', className = 'card_header'),
                    dcc.Loading(html.Div([
                                        html.Img(src = './static/EV-Station-2.jpg', 
                                                 id = 'ev_img',
                                                 className = 'station_img', 
                                                 style=dict(height = '200px', width = '100%'),),
                                        
                                        html.Div([
                                                 html.P(children = 'Select Map Pushpin', id = 'ev_name', className = 'station_name'),
                                                 html.P(children = 'to view details', id = 'ev_station', style = dict(opacity = 0.5)), 
                                                ], className = 'pl-2'),
            
                                        html.Hr(),
                                        
                                        dbc.Row([
                                                dbc.Col([
                                                        html.Img(src = './static/timetable-icon.png', className = 'ev_icon',  id = 'op_hour'),
                                                        dbc.Tooltip('Operating Hours', target = "op_hour", innerClassName = 'station_ttip'),
                                                        ], width = 3, className = 'p-2'),
                                                dbc.Col([
                                                        html.P(id = 'hour_info', className = 'ev_text'),
                                                        ], width = 9),
                                                ]),
                                        
                                        dbc.Row([
                                                dbc.Col([
                                                        html.Img(src = './static/payment-icon.png', className = 'ev_icon', id = 'payment'),
                                                        dbc.Tooltip('Acess', target = "payment", innerClassName = 'station_ttip'),
                                                        ], width = 3, className = 'p-2'),
                                                dbc.Col([
                                                        html.P(id = 'payment_info', className = 'ev_text'),
                                                        ], width = 9),
                                                ]),
        
                                        dbc.Row([
                                                dbc.Col([
                                                        html.Img(src = './static/operator-icon.png', className = 'ev_icon', id = 'operator'),
                                                        dbc.Tooltip('Operator', target = "operator", innerClassName = 'station_ttip'),
                                                        ], width = 3, className = 'p-2'),
                                                dbc.Col([
                                                        html.P(id = 'operator_info', className = 'ev_text'),
                                                        ], width = 9),
                                                ]),                                      
                                                            
                                        dbc.Row([
                                                dbc.Col([
                                                        html.Img(src = './static/review-icon.png', className = 'ev_icon', id = 'review'),
                                                        dbc.Tooltip("Customer's Review", target = "review", innerClassName = 'station_ttip'),
                                                        ], width = 3, className = 'p-2'),
                                                dbc.Col([
                                                        html.P(id = 'review_info', className = 'ev_text'),
                                                        ], width = 9),
                                                ]),            
                                    ],
                                className = 'station_info p-1', style = dict(height = '560px')), type="default", ),
                    ], className = 'card')

##################
# Vehicle Count and Interarrival Time
##################
card_tsplot = dbc.Card(
        [
                dbc.CardHeader('Vehicle Count and Interarrival Time', className = 'card_header'),
                dcc.Loading(
                                children = html.Div(dcc.Graph(id='ec_arrival_tsplot', style= dict(height = '255px'))),
                                type="default"),
        ],className = 'card mt-2')

##################
# Main Layout
##################
layout = html.Div([
        dbc.Row([
                dbc.Col([
                        bing_map,
                        station_summary,
                         ], width = 8),
                dbc.Col(station_card, width = 4),
                ], className = 'py-1'),
        html.Div(id='charge_intermediate',  className = 'd-none', children = pd.DataFrame().to_json()),
        ])