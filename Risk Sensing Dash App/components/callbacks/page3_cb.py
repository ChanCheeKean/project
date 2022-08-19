# Layout for forecasting page
import pandas as pd
import numpy as np
from dash.dependencies import Input, Output, State
from utils.plot_helper import get_ts_s1, get_mapbox, get_histrogram_x
from app import app
from datetime import datetime, timedelta
from utils.dash_helpers import parse_options
from utils.data_loader import fetch_data, cal_trust_score

path = './data/LN_amazon_processed_50k.pkl'
df_input = fetch_data(path, start=datetime.now()-pd.Timedelta(days=37), end=datetime.now())

##############################################################
### Update Dimension Dropdown, Triggered by Trust Pillars ###
##############################################################
@app.callback (
        [Output('pg3_input_cat', 'value'), Output('pg3_input_cat', 'options')],
        [Input('pg2_intermediate_map', 'children'), Input('pg3_input_dim', 'value'),]
)
def update_dropdown(json, input_pillar):
    df = pd.read_json(json)    
    df = df[df['Trust Dimension'].str.contains(input_pillar)]
    df['Category'] = df['Category'].apply(lambda x: [a for a in x.split('/')][0]).apply(lambda x: [a for a in x.split('(')][0])
    l = list(df['Category'].unique())
    l = ['All'] + l
    return l[0], parse_options(l)

################################################
### Update Table, Triggered by Trust Pillars ###
################################################
@app.callback (
        [Output('pg3_table_article', 'data'), Output('pg3_table_article', 'style_data_conditional')], 
        [Input('pg3_input_dim', 'value'), Input('pg3_input_cat', 'value'), Input('pg3_date-picker', 'start_date'), Input('pg3_date-picker', 'end_date')]
)

def update_table(inp_dim, inp_cat, start, end):
    df = df_input.copy()    
    df = df[df['Trust Dimension'].str.contains(inp_dim)]
    df['Category'] = df['Category'].apply(lambda x: [a for a in x.split('/')][0]).apply(lambda x: [a for a in x.split('(')][0])
    df['Trust Dimension'] = inp_dim
    
    if inp_cat == 'All':
        pass
    else:
        df = df[df['Category'].str.contains(inp_cat)]
    
    df = cal_trust_score(df, datetime.now()-pd.Timedelta(days=37), datetime.now(), w0=0.8, with_rec=False)    
    df = df[['title', 'publishedDate', 'Trust Dimension', 'Category', 'Topics', 'trust_score', 'coverage', 'f_sentiment', 'f_saliency', 'url_num', 'originalUrl']]   
    df['Topics'] = df['Topics'].str.capitalize()
    
    df.columns = ['TITLE', 'DATE', 'DIMENSION', 'CATEGORY', 'TOPICS', 'TRUST SCORE', 'COVERAGE', 'SENTIMENT', 'SALIENCY', 'URL #', 'LINK']
    df = df[(df['DATE'] >= start) & (df['DATE'] <= end)]
    df['DATE'] = df['DATE'].dt.strftime('%Y %b %d %H:%M')
    df['LINK'] = [f"[{x}]({x})" for x in df['LINK']]

    df = df.round(3)
    style = [
        {
            "if": {"state": "active"}, 
            "backgroundColor": "inherit!important", 
            "border": "none!important",
            },
       
        {
            'if': {'column_id': 'TITLE'},
            'textAlign': 'left',
            'padding': '0 10px',
            },
        
        {
            'if': {'column_id': 'lINK'},
            'textAlign': 'left',
            },
        
        {
            'if': {'column_id': 'TOPICS'},
            'maxWidth': '100px',
            },
        
        {
            'if': {'column_id': 'DATE'},
            'maxWidth': '100px',
            },
        
        {
            'if': {'column_id': 'CATEGORY'},
            'maxWidth': '100px',
            },
                
      ]
    return df.to_dict('records'), style