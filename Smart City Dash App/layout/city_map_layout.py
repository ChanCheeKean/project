import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import bing_maps_smartcity as bms
from data.bingmaps_data import pp_roadworks, pp_congestions, pp_webcams, pp_energy, pl_roadworks, pg_webcams

##################
# Row 0 - Functionality Tree
##################
func_tree = html.Div([
                    dbc.Button([
                            html.Img(src = './static/down-icon.png', className = 'icon d-inline-block mb-1', ),
                            ], id = 'overview_tree_button', outline=False, className = 'tree_button'),
                    dbc.Collapse([
                            dbc.Card([
                                    dbc.CardHeader('Functionality Tree', className = 'card_header'),
                                    html.Img(src='./static/Showcase UI Overview.jpg', style=dict(height = '500px')),
                                    ], className = 'card py-2')
                            ],id="overview_tree_collapse",)])

##################
# Map
##################
card_map = dbc.Card([dbc.CardHeader('City Detection Points', className = 'card_header'),
                     # return bingmap in callback
                     bms.BingMaps(
                         id = 'city-map',
                         polygons = pg_webcams,
                         polylines = pl_roadworks,
                         pushpins = pp_roadworks + pp_congestions + pp_webcams + pp_energy
                     )
                    ], className = 'card', style={'height': '510px'})

##################
# Data Summary
##################
card_info = dbc.Card(
        [dbc.CardHeader('Data Summary', className = 'card_header'),
         html.Div([
                 html.Span('13', style = dict(color = '#14A76C', fontSize = '1.8rem'), className = 'font-weight-bold pl-3 pt-2'),
                 html.Span('Detection Points', style = dict(fontSize = '1.0rem'), className = 'pl-3 text-white'),
                 ]),

        html.Div([
                 html.Span('2', style = dict(color = 'white', fontSize = '1.8rem'), className = 'font-weight-bold pl-3 pt-2'),
                 html.Span('Speed Camera', style = dict(fontSize = '1.0rem'), className = 'pl-3 text-white'),
                 ]),

         html.Div([
                 html.Span('7', style = dict(color = 'white', fontSize = '1.8rem'), className = 'font-weight-bold pl-3 pt-2'),
                 html.Span('Environmental Sensor', style = dict(fontSize = '1.0rem'), className = 'pl-3 text-white'),
                 ]),

        html.Div([
                 html.Span('2', style = dict(color = 'white', fontSize = '1.8rem'), className = 'pl-3 pt-2'),
                 html.Span('Surveillance Camera', style = dict(fontSize = '1.0rem'), className = 'pl-3 text-white'),
                 ]),

        html.Div([
                 html.Span('2', style = dict(fontSize = '1.8rem'), className = 'pl-3 pt-2 text-white-50'),
                 html.Span('Offline', style = dict(fontSize = '1.0rem'), className = 'pl-3 text-white'),
                 ]),

         ], style=dict(height = '250px'), className = 'card')

##################
# City Alert
##################
card_alert = dbc.Card(
        [dbc.CardHeader('Alert Log (Last 24 Hours)', className = 'card_header'),
         dbc.Row([
                 dbc.Col([
                         html.P('Event', className = 'text-white-50'),
                         html.P('Thunder Storm', className = 'text-white font-weight-bold small'),
                         html.P('Collision (Fatal)', className = 'text-white font-weight-bold small'),
                         html.P('Traffic Jam (>5km)', className = 'text-white font-weight-bold small'),
                         html.P('Road Work (Baldung-St)', className = 'text-white font-weight-bold small'),
                         ],width = 6),

                dbc.Col([
                         html.P('Severity', className = 'text-white-50',),
                         html.P('Minor', className = 'small', style = dict(color = '#14A76C')),
                         html.P('Critical', className = 'small',  style = dict(color = '#FC4445'),),
                         html.P('Major', className = 'small',  style = dict(color = '#FFE400'),),
                         html.P('Critical', className = 'small',  style = dict(color = '#FC4445'),),
                         ],width = 3),

                dbc.Col([
                         html.P('Date', className = 'text-white-50',),
                         html.P('3 Minutes', className = 'small text-white',),
                         html.P('8 Hours', className = 'small text-white',),
                         html.P('13 Hours', className = 'small text-white',),
                         html.P('22 Hours', className = 'small text-white',),
                         ],width = 3),

                 ], className = 'pl-2 pt-2')
         ], style=dict(height = '250px'), className = 'card mt-2')

##################
# Traffic Summary
##################
card_traffic = dbc.Card(
        [dbc.CardHeader('Traffic Data Summary (Last 5 minutes)', className = 'card_header'),
         html.Div([
                 html.Img(src = './static/accident-icon.png', className = 'icon d-inline-block mb-1', ),
                 html.Span('2', style = dict(color = '#FFE400', fontSize = '1.5rem'), className = 'pl-5'),
                 ], className = 'px-5 py-2'),

        html.Div([
                 html.Img(src = './static/roadblock-icon.png', className = 'icon d-inline-block'),
                 html.Span('4', style = dict(color = '#FFE400', fontSize = '1.5rem'), className = 'pl-5'),
                 ], className = 'px-5 py-2'),

        html.Div([
                 html.Img(src = './static/jam-icon.png', className = 'icon d-inline-block'),
                 html.Span('5', style = dict(color = '#FFE400', fontSize = '1.5rem'), className = 'pl-5'),
                 ], className = 'px-5 py-2'),

        ], className = 'card',style=dict(height = '260px'))

##################
# E-Charging Summary
##################
card_charge = dbc.Card(
        [dbc.CardHeader('E-Charging Data Summary (Last 5 minutes)', className = 'card_header'),


        ], className = 'card',style=dict(height = '260px'))


##################
# Environmental Summary
##################

card_env = dbc.Card(
        [dbc.CardHeader('Environmental Data Summary (Last 5 minutes)', className = 'card_header'),
        ], className = 'card',style=dict(height = '260px'))

##################
# Pop Out
##################
image = html.Img(src= f"https://www.schwaebisch-gmuend.de/files/upload/webcam/marktplatz1/gmuendcam.jpg?",
                 id = 'cm_pop_image',
                 style=dict(height = '300px', width = '100%'))

content = dbc.Row([
            dbc.Col(image, width = 6),
            dbc.Col([
                    html.H6('Information:', className = 'font-weight-bold'),
                    html.Hr(),
                    html.Div([
                            html.Span('Title: '),
                            html.Span( id = 'pop_title', className = 'pop_out_text'),
                            ], className = 'p-2'),

                    html.Div([
                            html.Span('Longitude: '),
                            html.Span(id = 'pop_longitude', className = 'pop_out_text'),
                            ], className = 'p-2'),

                    html.Div([
                            html.Span('Latitude: '),
                            html.Span(id = 'pop_latitude', className = 'pop_out_text'),
                            ], className = 'p-2'),

                    html.Div([
                            html.Span('Description: '),
                            html.Span(id = 'pop_desc', className = 'pop_out_text'),
                            ], className = 'p-2'),

                    ],width = 6)
            ], className = 'pr-4 pt-2')

pop_out_map = dbc.Alert(
            children = content,
            id="map_pop_out",
            dismissable=True,
            is_open=False,)

##################
# Main Layout
##################
layout = html.Div([
        dbc.Row([dbc.Col(func_tree)]),
        dbc.Row([
                dbc.Col(card_map,width = 8),
                dbc.Col([card_info, card_alert], width = 4),
                ], className = 'py-2'),

#                dbc.Row([
#                    dbc.Col(card_traffic,width = 4),
#                    dbc.Col(card_charge, width = 4),
#                    dbc.Col(card_env, width = 4),
#                ], className = 'py-2'),

        html.Div(pop_out_map),
        dcc.Interval(id='overview_interval', interval=30*1000, n_intervals=0),
        html.Div(id='overview_intermediate',  className = 'd-none'),
        ])
