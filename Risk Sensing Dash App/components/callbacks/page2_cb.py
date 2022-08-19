# Layout for forecasting page
import pandas as pd
import numpy as np
from dash.dependencies import Input, Output, State
from utils.plot_helper import get_ts_s1, get_mapbox, get_histrogram_x, get_bar_h, get_pie_chart
from app import app
import time
from datetime import datetime, timedelta
from utils.dash_helpers import parse_options
from dateutil.relativedelta import relativedelta
from utils.data_loader import fetch_data, cal_trust_score

# load real data
path = './data/LN_amazon_processed_50k.pkl'
df_input = fetch_data(path, start=datetime.now()-pd.Timedelta(days=37), end=datetime.now())

#####################################
### Update Map, Triggered by Data ###
#####################################
@app.callback (Output('trust_map', 'figure'), 
               [Input('pg2_intermediate_map', 'children')])

def generate_mapbox(json):   
    # plotting
    foo = pd.DataFrame([[37.09, -95.7, 40, 900], [35.87, 104.19, 55, 400], [56.14, -106.3, 80, 600], [51, 10.5, 90, 450], [55.4, -3.4, 60, 250], [40.4, -3.75, 75, 300]],
                       index=['United States', 'China', 'Canada', 'Germany', 'United Kingdom', 'Spain'], 
                       columns=['lat', 'lon', 'value', 'count'])
    
    return get_mapbox(lat=foo['lat'].values, 
                      lon=foo['lon'].values, 
                      size=(foo['count'] / 20).values,
                      color=foo['value'].values,
                      text=[f"Country: {x}<br>Total Counts: {y}<br>Trust Score: {z}" for x, y, z in zip(foo.index, foo['count'], foo['value'])], 
                      center_lat=45, 
                      center_lon=0, 
                      zoom=1.2, 
                      height=400)

####################################################
### Update Time Series, Triggered by Map and Tab ###
####################################################
@app.callback (
        Output('page2_ts_trust', 'figure'), 
        [Input('pg2_intermediate_map', 'children'), Input('trust_map', 'selectedData'), Input('ts_trust_tab', 'value')]
)
def update_ts_plot(json, selected_data, tab):
    # df = pd.read_json(json)[['published-at', 'salience_conf_score', 'sentiment_score_new_rounded']]
    df = df_input.copy()
    
    if tab == 'h':
        freq, leng ='1H', 24
        start = (datetime.now() - pd.Timedelta(hours=12))
        end = datetime.now()
        df = cal_trust_score(df, start, end, w0=0.8, with_rec=False)  
        alpha = 0.75

    elif tab == 'd':
        freq, leng ='1D', 30
        start = (datetime.now() - pd.Timedelta(days=37))
        end = datetime.now()
        df = cal_trust_score(df, start, end, w0=0.8, with_rec=False)  
        alpha = 0.3
    
    df = df[['publishedDate', 'trust_score']].set_index('publishedDate')
    df = df.resample(freq).mean().fillna(0)
    df = df.ewm(alpha=alpha).mean()
    df = df[-leng:]
    df.columns = ['Trust_Score']
    return get_ts_s1(df, 'Trust_Score', height=225, lw=5)

#############################################
### Update Density Plot, Triggered by Map ###
#############################################
@app.callback (Output('density_plot', 'figure'), Input('trust_map', 'selectedData'))

def update_dist_plot(selectedData):       
    df = df_input.copy()
    df = cal_trust_score(df, datetime.now()-pd.Timedelta(days=7), datetime.now(), w0=0.8, with_rec=False)
    df = df[['Trust Dimension', 'trust_score']]
    df.columns=['Dimension', 'Trust Score']
        
    lis = []
    for dim in ['Ability', 'Integrity', 'Purpose', 'Dependability']:
        foo = df[df['Dimension'].str.contains(dim)].copy()
        foo['Dimension'] = dim
        lis.append(foo)
    df = pd.concat(lis)
    
    fig = get_histrogram_x(df, 'Dimension', 'Trust Score', mode='overlay', height=300, bins=80, norm="probability", xtitle='Trust Score', ytitle='Prob Density',)
    return fig

#############################################
### Update Count Plot, Triggered by Map ###
#############################################
@app.callback (Output('pg2_count_bar', 'figure'), Input('trust_map', 'selectedData'))

def update_count_bar(selectedData):
    df = df_input.copy()
    df = cal_trust_score(df, datetime.now()-pd.Timedelta(days=7), datetime.now(), w0=0.8, with_rec=False) 
    df = df[['Trust Dimension', 'trust_score']]
    df.columns=['Dimension', 'Trust Score']
    
    lis = []
    for dim in ['Ability', 'Integrity', 'Purpose', 'Dependability']:
        foo = df[df['Dimension'].str.contains(dim)].copy()
        foo['Dimension'] = dim
        lis.append(foo)
    df = pd.concat(lis)
    
    df_positive = df[df['Trust Score'] > 0].copy()
    df_negative = df[df['Trust Score'] < 0].copy()
    
    df = pd.concat([df_positive.groupby('Dimension').count().T, df_negative.groupby('Dimension').count().T], axis=0)
    df.index = ['Positive', 'Negative']
    
    fig = get_bar_h(df, height=200, xtitle='Mention Counts')
    return fig

##################################################
### Update Pie Chart, Triggered by Map and Tab ###
##################################################
@app.callback (
        Output('page2_pie_chart', 'figure'), 
        [Input('trust_map', 'selectedData'), Input('pg2_pie_tab', 'value')])
def update_pie_chart(selected_data, tab):
    df = df_input.copy()
    df = cal_trust_score(df, datetime.now()-pd.Timedelta(days=7), datetime.now(), w0=0.8, with_rec=False)[['originalUrl', 'Trust Dimension', 'Category']]
    df = df[df['Trust Dimension'].str.contains(tab)].copy()
    df['Category'] = df['Category'].apply(lambda x: [a for a in x.split('/')][0]).apply(lambda x: [a for a in x.split('(')][0])
    df_group = df.groupby('Category')['originalUrl'].count().sort_values(ascending=False)
    fig = get_pie_chart(df_group, height=200)
    return fig