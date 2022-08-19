import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_daq as daq
import dash_html_components as html
import dash_table
from utils.dash_helpers import parse_options
import datetime as dt
from components.callbacks import playground_cb
import pandas as pd

#####################
### Data Selector ###
#####################
input_cov = html.Div(
                children = [
                        html.Div('Incl. Coverage: ', className='input_text mr-2'), 
                        dcc.Dropdown(
                            id='pg_input_cov', 
                            value='Yes', 
                            options = parse_options(['Yes', 'No']),
                            style = dict(display="inline-block", fontSize="0.8rem", width="10.5em", textAlign="center", verticalAlign="top"))
                        ], 
                className = 'd-inline-block mr-3')

input_method = html.Div(
                children = [
                        html.Div('Method: ', className='input_text mr-2'), 
                        dcc.Dropdown(
                            id='pg_input_method', 
                            value='additive', 
                            options = parse_options(['additive', 'multiplicative']),
                            style = dict(display="inline-block", fontSize="0.8rem", width="10.5em", textAlign="center", verticalAlign="top"))
                        ], 
                className = 'd-inline-block mr-3')

senti_weight = html.Div(
                children = [
                        html.Div('Senti Weight: ', className='input_text mr-2'), 
                         dcc.Input(
                            id='pg_input_senti_w', 
                            type='number',
                            value=0.8, 
                            min=0, 
                            max=1,
                            style = dict(display="inline-block", fontSize="0.8rem", width="10.5em", textAlign="center", verticalAlign="top"))
                        ], 
                className = 'd-inline-block mr-3')

saliency_up = html.Div(
                children = [
                        html.Div('Sal Multiplier (title): ', className='input_text mr-2'), 
                         dcc.Input(
                            id='pg_input_sal_mul', 
                            type='number',
                            value=1.5, 
                            min=1, 
                            max=2, 
                            step=0.1,
                            style = dict(display="inline-block", fontSize="0.8rem", width="10.5em", textAlign="center", verticalAlign="top"))
                        ], 
                className = 'd-inline-block mr-3')

saliency_filter = html.Div(
                children = [
                        html.Div('Sal Filter: ', className='input_text mr-2'), 
                         dcc.Input(
                            id='pg_input_sal_filter', 
                            type='number',
                            value=0, 
                            min=0, 
                            max=1,
                            step=0.1,
                            style = dict(display="inline-block", fontSize="0.8rem", width="10.5em", textAlign="center", verticalAlign="top"))
                        ],
                className = 'd-inline-block mr-3')

senti_filter = html.Div(
                children = [
                        html.Div('Senti Filter: ', className='input_text mr-2'), 
                         dcc.Input(
                            id='pg_input_senti_filter', 
                            type='number',
                            value=0.05, 
                            min=0, 
                            max=1,
                            style = dict(display="inline-block", fontSize="0.8rem", width="10.5em", textAlign="center", verticalAlign="top"))
                        ], 
                className = 'd-inline-block mr-3')

####################
### Density Plot ###
####################
density_plot = dbc.Card([
    dbc.CardHeader('Density Plot (Sentiments vs Saliency vs Coverage)', className='card_header'),
    dcc.Loading(dcc.Graph(id='pg_density_plot'), type='default'),
    ], className='card')

############################
### Comparison Line Plot ###
############################
line_plot = dbc.Card([
    dbc.CardHeader('Comparison (with Title vs w/o Title)', className='card_header'),
    dcc.Loading(dcc.Graph(id='pg_line_plot'), type='default'),
    ], className='card')

################################
### Density Plot for Pillars ###
################################
density_plot_pillars = dbc.Card([
    dbc.CardHeader('Density Plot (4 Pillars)', className='card_header'),
    dcc.Loading(dcc.Graph(id='pg_density_plot_2'), type='default'),
    ], className='card')

###############
### TS Plot ###
###############
ts_plot = dbc.Card([
    dbc.CardHeader('Time Series Plot', className='card_header'),
    dcc.Loading(dcc.Graph(id='pg_ts_plot'), type='default'),
    ], className='card')


###############
### TS Plot ###
###############
input_xaxis = html.Div(
                children = [
                        html.Div('X-Axis: ', className='input_text mr-2'), 
                        dcc.Dropdown(
                            id='pg_input_vs_x', 
                            value='Coverage', 
                            options = parse_options(['MozRank', 'Coverage', 'Saliency Score', 'Sentiment Score', 'Article Count', 'Trust Score']),
                            style = dict(display="inline-block", fontSize="0.8rem", width="10.5em", textAlign="center", verticalAlign="top"))
                        ], 
                className = 'd-inline-block mr-3')

input_yaxis = html.Div(
                children = [
                        html.Div('Y-Axis: ', className='input_text mr-2'), 
                        dcc.Dropdown(
                            id='pg_input_vs_y', 
                            value='Trust Score', 
                            options = parse_options(['MozRank', 'Coverage', 'Saliency Score', 'Sentiment Score', 'Article Count', 'Trust Score']),
                            style = dict(display="inline-block", fontSize="0.8rem", width="10.5em", textAlign="center", verticalAlign="top"))
                        ], 
                className = 'd-inline-block mr-3')

vs_plot = dbc.Card([
    dbc.CardHeader('X-Y Comparison Plot', className='card_header'),
    dcc.Loading([html.Div([input_xaxis, input_yaxis], className = 'd-inline-block mt-2 ml-4'), dcc.Graph(id='pg_vs_plot')], type='default'),
    ], className='card')

##########################
### Table Input Group ####
##########################
input_pillar = html.Div(
                children = [
                        html.Div('TRUST DIMENSION: ', className='input_text mr-2'), 
                        dcc.Dropdown(
                            id='pg_input_dim', 
                            value='Ability', 
                            options = parse_options(['Ability', 'Dependability', 'Integrity', 'Purpose']),
                            style = dict(display="inline-block", fontSize="0.8rem", width="12em", textAlign="center", verticalAlign="top"))
                        ], 
                className = 'd-inline-block mr-3')

input_dim = html.Div(
                children = [
                        html.Div('TRUST CATEGORY: ', className='input_text mr-2'), 
                        dcc.Dropdown(
                            id='pg_input_cat', 
                            style = dict(display="inline-block", fontSize="0.8rem", width="20em", textAlign="center", verticalAlign="top"))
                        ], 
                className = 'd-inline-block mr-3')

date_picker = html.Div(
                children = [
                        html.Div(children ='DATE: ', className = 'input_text mr-2'), 
                        dcc.DatePickerRange(id='pg_date-picker', 
                                            min_date_allowed=dt.datetime.now() - dt.timedelta(days=31), 
                                            max_date_allowed=dt.datetime.now(), 
                                            display_format='DD/MM/YYYY',
                                            start_date=dt.datetime.now() - dt.timedelta(days=7),
                                            end_date = dt.datetime.now(), 
                                            initial_visible_month = dt.datetime.now())
                        ],
                className = 'd-inline-block mr-3')

#####################
### Article Table ###
#####################
table1 = dash_table.DataTable(id='pg_table_article',
                         columns = [{"name": i, "id": i} for i in ['GROUPID', 'TITLE', 'DATE', 'DIMENSION', 'CATEGORY', 'TOPICS', 'TRUST SCORE', 'COVERAGE', 'SENTIMENT', 'SALIENCY', 'MENTION RATIO', 'URL #']] + [{"name": 'LINK', "id": 'LINK', 'type':'text', 'presentation': 'markdown'}],
                         sort_action='native',
                         style_as_list_view=True,
                         style_table={'height': '400px', 'overflowY': 'auto', 'overflowX': 'auto'},
                         style_cell=dict(textAlign='center', padding='5px', color='white', backgroundColor='#303030', fontSize='16px', 
                                         height='auto', whiteSpace='normal', maxWidth='300px'), 
                         style_header=dict(fontWeight='bold', color='white', fontSize='15px', borderBottom='2px solid white'))

card1 = dbc.Card([
    dbc.CardHeader(['ARTICLES LIBRARY'], className = 'card_header'),
    dcc.Loading([html.Div([input_pillar, input_dim, date_picker], className='m-3'),
                 table1
                 ], type='default'),
    ], className = 'card')

############
### Data ###
############
index_mapping = pd.read_csv('./data/index_term_category.csv')

########################
### Combining Layout ###
########################
layout = html.Div([
        html.Div([input_cov, input_method, senti_weight, saliency_up, saliency_filter, senti_filter], className='mt-2'), 
        html.Div(id='pg_intermediate_map',  className='d-none', children=index_mapping.to_json()),
        
        dbc.Row([
            dbc.Col(density_plot, width=6, className='px-2'),
            dbc.Col(line_plot, width=6, className='px-2'),
            ], className='mt-4'),
        
        
        dbc.Row([
            dbc.Col(density_plot_pillars, width=6, className='px-2'),
            dbc.Col(ts_plot, width=6, className='px-2'),
            ], className='mt-4'),
        
        dbc.Row([
            dbc.Col(vs_plot, width=12),
            ], className='mt-3'),
        
        dbc.Row([
            dbc.Col(card1, width=12),
            ], className='mt-3'),
        
        ], className='m-4')