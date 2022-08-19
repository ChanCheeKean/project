import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import dash_daq as daq
from datetime import datetime, timedelta
from utils.dash_helpers import parse_options

##################
# Data Selector
##################
region_picker = html.Div(
                children = [
                        html.Div('Region: ', className = 'inputGroup__label d-inline-block'), 
                        dcc.Dropdown (
                                id = 'region_picker', 
                                style = dict(display = 'inline-block'), 
                                className = 'inputGroup select', 
                                options = parse_options(['Gmünd East', 'Gmünd North', 'Gmünd South West']),
                                value = 'Gmünd East', 
                                )
                        ], 
                className = 'inputGroup inline d-inline-block')

id_picker = html.Div(
                children = [
                        html.Div('Car Park ID: ', className = 'inputGroup__label d-inline-block'), 
                        dcc.Dropdown (
                                id = 'carpark_id_picker', 
                                style = dict(display = 'inline-block'), 
                                className = 'inputGroup select', 
                                options = parse_options(['E020','W052','S009', 'N078']),
                                value = 'N078', 
                                )
                        ], 
                className = 'inputGroup inline d-inline-block')

date_picker =  html.Div(
                children = [
                        html.Div(children ='Dates: ', className = 'inputGroup__label d-inline-block'), 
                        dcc.DatePickerRange(id='carpark_date-picker', 
                                            min_date_allowed = datetime.now() - timedelta(days = 90), 
                                            max_date_allowed = datetime.now(), 
                                            display_format='DD/MM/YYYY',
                                            start_date = datetime.now() - timedelta(days = 10),
                                            end_date = datetime.now(), 
                                            initial_visible_month = datetime.now(), 
                                            className = 'inputGroup select date-picker d-inline-block'),
                        ],
                className = 'inputGroup inline d-inline-block')

submit_button = dbc.Button(id='carpark_submit', children='Submit', n_clicks=0, color="primary", className = 'd-inline-block')

data_selector = [id_picker, date_picker, submit_button]

##################
# Traffic Volume Heatmap
##################
# heatmap
hm_layout = dbc.Card([
        dbc.CardHeader('Car Volume Heatmap', className = 'card_header'),
        dcc.Loading(
                children = dcc.Graph (id = 'parking_hm', style=dict(height = '350px', width = '98%')),
                type="default"),
        ],className = 'card')
                
##################
# Parking Occupancy Bar
##################
bar1 = daq.GraduatedBar(
        vertical=True, 
        value = 7,
        label = 'Working Day',
        labelPosition = 'bottom',
        size = 200,
        showCurrentValue=True,
        color={"gradient":True,"ranges":{"green":[0,5],"yellow":[5,8],"red":[8,10]}},
        id = 'park_work_bar', className = 'parking_bar',
        )  

bar2 = daq.GraduatedBar(
        vertical=True, 
        value = 10,
        label = 'Holiday Business Day',
        labelPosition = 'bottom',
        size = 200,
        showCurrentValue=True,
        color={"gradient":True,"ranges":{"green":[0,5],"yellow":[5,8],"red":[8,10]}},
        id = 'park_school_bar', className = 'parking_bar',
        )  

bar3 = daq.GraduatedBar(
        vertical=True, 
        value = 3,
        label = 'Bank Holiday',
        labelPosition = 'bottom',
        size = 200,
        showCurrentValue=True,
        color={"gradient":True,"ranges":{"green":[0,5],"yellow":[5,8],"red":[8,10]}},
        id = 'park_hol_bar',className = 'parking_bar',
        )  

occupancy_bar = dbc.Card([
                    dbc.CardHeader('Parking Lots Occupancy', className = 'card_header'),
                    dcc.Loading(
                            children =  dbc.Row([
                                                dbc.Col(bar1, width = 4),
                                                dbc.Col(bar2, width = 4),
                                                dbc.Col(bar3, width = 4),
                                                ], className = 'pt-4', style=dict(height = '350px')),
                            type="default"),
                    ], className = 'card')

##################
# Main Layout
##################
layout = html.Div([
        html.Div(data_selector, className = 'pb-2'),
        dbc.Row([
                dbc.Col(hm_layout, width = 8),
                dbc.Col(occupancy_bar, width = 4),
                ], className = 'py-1'),       
        html.Div(id='carpark_intermediate',  className = 'd-none'),
        ])