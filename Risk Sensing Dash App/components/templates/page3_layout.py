import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_daq as daq
import dash_html_components as html
import dash_table
import datetime as dt
from components.callbacks import page3_cb
from utils.dash_helpers import parse_options

####################
### Input Group ####
####################
input_pillar = html.Div(
                children = [
                        html.Div('TRUST DIMENSION: ', className='input_text mr-2'), 
                        dcc.Dropdown(
                            id='pg3_input_dim', 
                            value='Ability', 
                            options = parse_options(['Ability', 'Dependability', 'Integrity', 'Purpose']),
                            style = dict(display="inline-block", fontSize="0.8rem", width="12em", textAlign="center", verticalAlign="top"))
                        ], 
                className = 'd-inline-block mr-3')

input_dim = html.Div(
                children = [
                        html.Div('TRUST CATEGORY: ', className='input_text mr-2'), 
                        dcc.Dropdown(
                            id='pg3_input_cat', 
                            style = dict(display="inline-block", fontSize="0.8rem", width="20em", textAlign="center", verticalAlign="top"))
                        ], 
                className = 'd-inline-block mr-3')

date_picker = html.Div(
                children = [
                        html.Div(children ='DATE: ', className = 'input_text mr-2'), 
                        dcc.DatePickerRange(id='pg3_date-picker', 
                                            min_date_allowed=dt.datetime.now() - dt.timedelta(days=31), 
                                            max_date_allowed=dt.datetime.now(), 
                                            display_format='DD/MM/YYYY',
                                            start_date=dt.datetime.now() - dt.timedelta(days=7),
                                            end_date = dt.datetime.now(), 
                                            initial_visible_month = dt.datetime.now())
                        ],
                className = 'd-inline-block mr-3')

#########################
### Article Table ###
#########################
table1 = dash_table.DataTable(id='pg3_table_article',
                         columns = [{"name": i, "id": i} for i in ['TITLE', 'DATE', 'DIMENSION', 'CATEGORY', 'TOPICS', 'TRUST SCORE', 'COVERAGE', 'SENTIMENT', 'SALIENCY', 'URL #']] + [{"name": 'LINK', "id": 'LINK', 'type':'text', 'presentation': 'markdown'}],
                         sort_action='native',
                         style_as_list_view=True,
                         style_table={'height': '480px', 'overflowY': 'auto', 'overflowX': 'auto'},
                         style_cell=dict(textAlign='center', padding='5px', color='white', backgroundColor='#303030', fontSize='16px', 
                                         height='auto', whiteSpace='normal', maxWidth='300px'), 
                         style_header=dict(fontWeight='bold', color='white', fontSize='15px', borderBottom='2px solid white'))
card1 = dbc.Card([
    dbc.CardHeader(['ARTICLES LIBRARY'], className = 'card_header'),
    dcc.Loading(table1, type='default'),
    ], className = 'card')

########################
### Combining Layout ###
########################
layout = html.Div([
        html.Div([input_pillar, input_dim, date_picker], className='mt-2'), 
        dbc.Row([
            dbc.Col(card1, width=12),
            ], className='mt-3'),       
        ], className='hidden_scroll')