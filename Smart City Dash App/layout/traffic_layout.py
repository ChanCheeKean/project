import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from datetime import datetime, timedelta
import pandas as pd

##################
# Row 0 - Functionality Tree
##################
func_tree = html.Div([
                    dbc.Button([
                            html.Img(src = './static/down-icon.png', className = 'icon d-inline-block mb-1', ), 
                            ], id = 'traffic_tree_button', outline=False, className = 'tree_button'),
                    dbc.Collapse([  
                            dbc.Card([
                                    dbc.CardHeader('Functionality Tree', className = 'card_header'),
                                    dbc.Row([
                                            dbc.Col(
                                                    html.Img(src='./static/Showcase UI Traffic - no Induction.jpg', style=dict(height = '500px', width = '100%')), 
                                                    width = 6,
                                                    className = 'pr-1'),
                                                    
                                            dbc.Col(
                                                    html.Img(src='./static/Showcase UI Traffic - with Induction.jpg', style=dict(height = '500px', width = '100%')), 
                                                    width = 6,
                                                    className = 'pl-1'),
                                            ]),
                                    
                                    ], className = 'card my-2')
                            ],id="traffic_tree_collapse",)])

##################
# Detection and Induction Loop
##################
bottom_bar = html.Div([dcc.Tabs([
                                dcc.Tab(label = 'Baldung Street', className = 'bot_tab_item', selected_className='bot_tab_activated', value = 'b'),
                                dcc.Tab(label = 'Gmuend Market', className = 'bot_tab_item', selected_className='bot_tab_activated', value = 'c'),
                                dcc.Tab(label = 'Unicorn Tunnel', className = 'bot_tab_item', selected_className='bot_tab_activated', value = 'd'),
                                dcc.Tab(label = 'Kings Street', className = 'bot_tab_item', selected_className='bot_tab_activated', value = 'a'),
                                ], className = 'bot_tab_nav', id="traffic_tabs", value = 'b'),
                ])

card_car_detect = dbc.Card([
                        dbc.CardHeader('Object Detection', className = 'card_header'),
                        html.Div(id = 'spot_content'),
                        html.Div(bottom_bar, ),
                        ], className = 'card')

##################
# Traffic Events
##################
card_car_event = dbc.Card([
                        dbc.CardHeader('Traffic Event', className = 'card_header'),
                        html.Div([
                                dbc.Button([
                                    html.Img(src = './static/accident-icon.png', className = 'icon d-inline-block mb-1', ), 
                                    html.Span('Collisions'),
                                    ], className = 'traffic_alert', id = 'collision_button', outline=False),
        
                                dbc.Collapse([  
                                         html.P(f'B29 {(datetime.now() - timedelta (minutes = 323)).strftime("%A %d %B %H%M")}', className = 'alert_collapse'),
                                         html.P(f'Marktplatz {(datetime.now() - timedelta (hours = 32)).strftime("%A %d %B %H%M")}', className = 'alert_collapse'),
                                        ],
                                        id="collision_collapse", is_open = True),
    
    
                                dbc.Button([
                                    html.Img(src = './static/roadblock-icon.png', className = 'icon d-inline-block mb-1', ), 
                                    html.Span('Roadblock', ),
                                    ], className = 'traffic_alert', id = 'rb_button', outline=False),
                                        
                                dbc.Collapse([  
                                         html.P(f'Klosterberg {(datetime.now() - timedelta (minutes = 12)).strftime("%A %d %B %H%M")}', className = 'alert_collapse'),
                                        ],
                                        id="rb_collapse",),
    
                                 dbc.Button([
                                    html.Img(src = './static/jam-icon.png', className = 'icon d-inline-block mb-1', ), 
                                    html.Span('Congestion', ),
                                    ], className = 'traffic_alert', id = 'congestion_button', outline=False),
                                        
                                dbc.Collapse([  
                                        html.P(f'Waisenhausgasse {(datetime.now() - timedelta (minutes = 630)).strftime("%A %d %B %H%M")}', className = 'alert_collapse'),
                                        html.P(f'Klosterberg {(datetime.now() - timedelta (hours = 8)).strftime("%A %d %B %H%M")}', className = 'alert_collapse'),
                                        html.P(f'B29 {(datetime.now() - timedelta (days = 1)).strftime("%A %d %B %H%M")}', className = 'alert_collapse'),
                                        ],
                                        id="congestion_collapse",),
    
                                ], className = 'alert_box'),
                        ], className = 'card', style=dict(height = '200px'))

##################
# PieChart and Traffic Info
##################
card1 = html.Div([
        html.P('Daily Peak Period', className = 'font-weight-bold text-left p-0 pl-2 text-white small'),
        html.H5('07:18 AM | 04:13 PM',  className = 'font-weight-bold p-0 pl-2 text-warning'),
        ], className = 'text-black text-center', )

card2 = html.Div([
        html.P('Avg Velocity', className = 'font-weight-bold text-left p-0 pl-2 text-white text-white small'),
        html.H5('45.8 km/h',  className = 'font-weight-bold p-0 pl-2 text-warning text-white', id= 'avg_speed'),
        ], className = 'text-black text-center', )
                                
pie_row = dcc.Graph (id = 'traffic_pie_chart', style = dict(height = '180px'))

info_col = html.Div([
        html.Div(card1),
        html.Div(card2),
        ], className = 'px-1 py-1')

card_car_summary = dbc.Card([
                        dbc.CardHeader('Traffic Information', className = 'card_header'),
                        dcc.Loading(
                                children =  dbc.Row([
                                        dbc.Col([info_col],width=6),
                                        dbc.Col([pie_row],width=6),
                                        ]), type="default"),
                        ], className = 'card')
        
##################
# Vehicle Counts
##################
card_car_info = dbc.Card([
                        dbc.CardHeader('Vehicle Counts (Bar Chart)',className = 'card_header'),
                        dcc.Loading(
                            children =   dcc.Graph(id = 'sensor_bar_plot', style=dict(height = '260px')),
                            type="default"),
                        ], className = 'card')

##################
# Traffic Volume
##################                           
bottom_bar = html.Div([dcc.Tabs([
                                dcc.Tab(label = 'Hourly', className = 'bot_tab_item', selected_className='bot_tab_activated', value='h'),
                                dcc.Tab(label = 'Daily', className = 'bot_tab_item', selected_className='bot_tab_activated', value='d'),
                                dcc.Tab(label = 'Monthly', className = 'bot_tab_item', selected_className='bot_tab_activated', value='m'),
                                ], className = 'bot_tab_nav', id="trafficv_tabs", value='h'),
                ])                                

card_traffic_vol = dbc.Card([
                        dbc.CardHeader('Timely Average Traffic Volume',className = 'card_header'),
                        bottom_bar,
                        dcc.Loading(
                                children =   dcc.Graph(id = 'traffic_ts_plot', style=dict(height = '220px')),
                                type="default"),
                        ], className = 'card'),

##################
# Main Layout
##################
layout = html.Div([
        dbc.Row([dbc.Col(func_tree)]),
        dbc.Row([dbc.Col(card_car_detect ,width = 6),
                 dbc.Col([
                         dbc.Row(dbc.Col(card_car_event, width = 12), ),
                         dbc.Row(dbc.Col(card_car_summary, width = 12), className = 'pt-2'),
                         
                         ], width = 6),
                 ], className = 'py-2'),
        dbc.Row([
                dbc.Col(card_car_info, width = 6),
                dbc.Col(card_traffic_vol, width = 6),
                ], className = 'py-2'),
    
        dcc.Interval(id='traffic_interval', interval = 10*1000, n_intervals=1),
        html.Div(id='test',  className = 'd-none'),
        html.Div(id='traffic_intermediate',  className = 'd-none'),
        ])