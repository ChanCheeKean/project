import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_daq as daq
import dash_html_components as html
import dash_table
from utils.dash_helpers import parse_options
import datetime as dt
from components.callbacks import page1_cb

#####################
### Data Selector ###
#####################
input_brand = html.Div(
                children = [
                        html.Div('BRAND: ', className='input_text mr-2'), 
                        dcc.Dropdown(
                            id='input_brand', 
                            value='Amazon', 
                            options = parse_options(['Amazon', 'AstraZeneca', 'Facebook', 'Shell', 'Unilever']),
                            style = dict(display="inline-block", fontSize="0.8rem", width="10.5em", textAlign="center", verticalAlign="top"))
                        ], 
                className = 'd-inline-block mr-3')

input_country = html.Div(
                children = [
                        html.Div('COUNTRY: ', className = 'input_text mr-2'), 
                        dcc.Dropdown(
                            id='input_country', 
                            value='United States', 
                            options = parse_options(['United States', 'Germany', 'United Kingdom', 'Spain']),
                            style = dict(display="inline-block", fontSize="0.8rem", width="12em", textAlign="center", verticalAlign="top"))
                        ], 
                className = 'd-inline-block mr-3')

input_trust = html.Div(
                children = [
                        html.Div('TRUST DIMENSION: ', className='input_text mr-2'), 
                        dcc.Dropdown(
                            id='input_dim_pg1', 
                            value='Overall', 
                            options = parse_options(['Overall', 'Ability', 'Dependability', 'Integrity', 'Purpose', 'Self']),
                            style = dict(display="inline-block", fontSize="0.8rem", width="12em", textAlign="center", verticalAlign="top"))
                        ], 
                className = 'd-inline-block mr-3')

date_picker = html.Div(
                children = [
                        html.Div(children ='DATE: ', className = 'input_text mr-2'), 
                        dcc.DatePickerRange(id='pg1_date-picker', 
                                            min_date_allowed=dt.datetime.now() - dt.timedelta(days=100), 
                                            max_date_allowed=dt.datetime.now(), 
                                            display_format='DD/MM/YYYY',
                                            start_date=dt.datetime.now() - dt.timedelta(days = 7),
                                            end_date = dt.datetime.now(), 
                                            initial_visible_month = dt.datetime.now())
                        ],
                className = 'd-inline-block mr-3')

submit_button = dbc.Button(id='input_submit', children='Submit', n_clicks=0, outline=True, color="primary", className = 'submit_but d-inline-block')

########################
### Trust Barometers ###
########################
meter = daq.Gauge(color={"gradient":True, "ranges":{"red":[-100, -50], "gold":[-50, 50], "green":[50, 100]}},
                        label='TRUST BAROMETER', showCurrentValue=True, units='%',
                        scale={'start':-100, 'interval':10,}, size=450,
                        value=43.2, max=100, min=-100, id='trust_gauge', labelPosition='top',
                        # style=dict(display = 'inline-block'), 
                        className = 'pt-3 gauge')

trust_meter = dbc.Card([
    # dbc.CardHeader(['Trust Radar', ], className = 'card_header'),
    meter,
    ], className = 'card')

###################
### Radar Chart ###
###################
paid_radar = dbc.Card([
    # dbc.CardHeader(['Trust Radar', ], className = 'card_header'),
    dcc.Loading(dcc.Graph(id='pg1_radar'))
    ], className = 'card')

#########################
### Competition Table ###
#########################

### Ability ###
tooltip1 = dbc.Tooltip(
    "Functional trust. Is your brand good at what it does? Is it competent?", 
    target="ability_icon",
    style = dict(background='#82827e'),
    placement='right')

table = dash_table.DataTable(id='table_1', 
                         columns = [{"name": i, "id": i} for i in ['BRANDS' , 'SCORES', 'RANKS', 'CHANGES']],
                         # style_as_list_view=True,
                         style_table=dict(height='220px', overflowY='auto', width='85%', margin='auto'),
                         style_cell=dict(textAlign='center', padding='2px', color='white', backgroundColor='#323232', fontSize='15px', border='none'), 
                         style_header=dict(fontWeight='bold', color='white', fontSize='14px', borderBottom='1px solid white'))

card_table = dbc.Card([
    # dbc.CardHeader(['Ranking: Ability', ], className = 'card_header'),
    dcc.Loading(table, type='default'),
    ], className = 'card mt-3')

########################
### Combining Layout ###
########################
layout = html.Div([
        html.Div([input_brand, input_country, input_trust, date_picker], className='mt-2'),
        
        dbc.Row([
            dbc.Col(trust_meter, width=7, className='px-2'),
            dbc.Col([paid_radar, card_table], width=5, className='px-2'),
            # dbc.Col([], width=4),
            ], className='mt-4'),        
        # dbc.Row([
        #     dbc.Col(card1, width=3),
        #     dbc.Col(card2, width=3),
        #     dbc.Col(card3, width=3),
        #     dbc.Col(card4, width=3),
        #     ], className = 'py-1 mt-4'),   
        
        ], className='hidden_scroll')
