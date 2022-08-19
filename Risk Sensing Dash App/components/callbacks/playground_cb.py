# Layout for forecasting page
import pandas as pd
import numpy as np
from dash.dependencies import Input, Output, State
from app import app
import time
from datetime import datetime, timedelta
from utils.dash_helpers import parse_options
from dateutil.relativedelta import relativedelta
from utils.data_loader import fetch_data, cal_trust_score
from utils.plot_helper import get_ts_plot, get_dist_plot, get_histrogram_x, get_ts_s1, get_joint_plot

# load real data
path = './data/LN_amazon_processed_50k.pkl'
df_input = fetch_data(path, start=datetime.now()-pd.Timedelta(days=37), end=datetime.now())

################################################
### Update Density Plot, Triggered by Input ###
################################################
@app.callback (Output('pg_density_plot', 'figure'), 
               [Input('pg_input_sal_mul', 'value'), Input('pg_input_sal_filter', 'value'), Input('pg_input_senti_filter', 'value'),])

def update_senti_sal_density_plot(sal_w, sal_thres, senti_thres):       
    df = df_input.copy()
    df = cal_trust_score(df, datetime.now()-pd.Timedelta(days=7), datetime.now(), w0=0.8, method='additive', 
                         sal_filter=float(sal_thres), up_weight=float(sal_w), senti_filter=float(senti_thres), with_rec=False, with_cov=True)
    df = df[['f_sentiment', 'f_saliency', 'coverage']]
    df.columns=['Sentiment', 'Saliency', 'Coverage']
    fig = get_dist_plot(df, xtitle='Scores', ytitle='Density', height=300, bins=100, show_hist=False, show_rug=False, curve_type='kde')
    return fig

################################################
### Update Density Plot, Triggered by Input ###
################################################
@app.callback (Output('pg_line_plot', 'figure'), Input('pg_input_sal_mul', 'value'))

def update_line_plot(sal_w):       
    df = pd.DataFrame({'Score' : np.arange(0, 1.05, 0.05)})
    df['w/o Title'] = df['Score'] * 2 - 1    
    df['with Title'] = df['Score'] * float(sal_w) * 2 - 1
    df['with Title'] = [1 if x > 1 else x for x in df['with Title']]
    df.set_index('Score', inplace=True)
    fig = get_ts_plot(df, height=300, hover_mode='x', legend_bool=True, xtick=0, drag_mode='zoom')
    return fig

###############################################
### Update Density Plot, Triggered by Input ###
###############################################
@app.callback (Output('pg_density_plot_2', 'figure'), 
               [Input('pg_input_cov', 'value'), Input('pg_input_method', 'value'), Input('pg_input_senti_w', 'value'), 
                Input('pg_input_sal_mul', 'value'), Input('pg_input_sal_filter', 'value'), Input('pg_input_senti_filter', 'value'),])

def update_dist_plot(cov_in, method, senti_w, sal_w, sal_filter, senti_fil):
    
    if cov_in == 'Yes':
        with_cov = True
    else:
        with_cov = False
    
    df = df_input.copy()
    df = cal_trust_score(df, datetime.now()-pd.Timedelta(days=7), datetime.now(), w0=float(senti_w), method=method, 
                         sal_filter=float(sal_filter), up_weight=float(sal_w), senti_filter=float(senti_fil), with_rec=False, with_cov=with_cov)
    
    df = df[['Trust Dimension', 'trust_score']]
    df.columns=['Dimension', 'Trust Score']
    lis = []
    for dim in ['Ability', 'Integrity', 'Purpose', 'Dependability']:
        foo = df[df['Dimension'].str.contains(dim)].copy()
        foo['Dimension'] = dim
        lis.append(foo)
    df = pd.concat(lis)
    fig = get_histrogram_x(df, 'Dimension', 'Trust Score', mode='overlay', height=300, bins=80, norm="probability", xtitle='Trust Score', ytitle='Prob Density')
    return fig

##############################################
### Update Time Series, Triggered by Input ###
##############################################
@app.callback (
        Output('pg_ts_plot', 'figure'), 
        [Input('pg_input_cov', 'value'), Input('pg_input_method', 'value'), Input('pg_input_senti_w', 'value'), 
         Input('pg_input_sal_mul', 'value'), Input('pg_input_sal_filter', 'value'), Input('pg_input_senti_filter', 'value'),])
def update_ts_plot(cov_in, method, senti_w, sal_w, sal_filter, senti_fil):
    # df = pd.read_json(json)[['published-at', 'salience_conf_score', 'sentiment_score_new_rounded']]
    df = df_input.copy()

    if cov_in == 'Yes':
        with_cov = True
    else:
        with_cov = False

    start = (datetime.now() - pd.Timedelta(days=37))
    freq, leng ='1D', 30
    alpha = 0.3
    end = datetime.now()
    df = cal_trust_score(df, start, end, w0=float(senti_w), method=method, 
                         sal_filter=float(sal_filter), up_weight=float(sal_w), senti_filter=float(senti_fil), with_rec=False, with_cov=with_cov)

    df = df[['publishedDate', 'trust_score']].set_index('publishedDate')
    df = df.resample(freq).mean().fillna(0)
    df = df.ewm(alpha=alpha).mean()
    df = df[-leng:]
    df.columns = ['Trust_Score']
    return get_ts_s1(df, 'Trust_Score', height=300, lw=5)

##########################################
### Update Vs Plot, Triggered by Input ###
##########################################
@app.callback (
        Output('pg_vs_plot', 'figure'), 
        [Input('pg_input_cov', 'value'), Input('pg_input_method', 'value'), Input('pg_input_senti_w', 'value'), 
         Input('pg_input_sal_mul', 'value'), Input('pg_input_sal_filter', 'value'), Input('pg_input_senti_filter', 'value'),
         Input('pg_input_vs_x', 'value'), Input('pg_input_vs_y', 'value'),])

def update_vs_plot(cov_in, method, senti_w, sal_w, sal_filter, senti_fil, col_x, col_y):
    # df = pd.read_json(json)[['published-at', 'salience_conf_score', 'sentiment_score_new_rounded']]
    df = df_input.copy()

    if cov_in == 'Yes':
        with_cov = True
    else:
        with_cov = False
        df['coverage'] = df['coverage_rank'].astype(float)  / 10
        df['url_num'] = df.groupby(['duplicateGroupId', 'title'])['originalUrl'].transform('count')

    start = (datetime.now() - pd.Timedelta(days=7))
    end = datetime.now()
    df = cal_trust_score(df, start, end, w0=float(senti_w), method=method, 
                          sal_filter=float(sal_filter), up_weight=float(sal_w), senti_filter=float(senti_fil), with_rec=False, with_cov=with_cov)

    df = df[['coverage_rank', 'coverage', 'f_saliency', 'f_sentiment', 'url_num', 'trust_score']]
    df.columns = ['MozRank', 'Coverage', 'Saliency Score', 'Sentiment Score', 'Article Count', 'Trust Score']
    
    return get_joint_plot(df[col_x], df[col_y], xtitle=col_x, ytitle=col_y, height=400)

##############################################################
### Update Dimension Dropdown, Triggered by Trust Pillars ###
##############################################################
@app.callback (
        [Output('pg_input_cat', 'value'), Output('pg_input_cat', 'options')],
        [Input('pg_intermediate_map', 'children'), Input('pg_input_dim', 'value'),]
)
def update_dropdown(json, input_pillar):
    df = pd.read_json(json)
    df = df[df['Trust Dimension'].str.contains(input_pillar)]
    df['Category'] = df['Category'].apply(lambda x: [a for a in x.split('/')][0]).apply(lambda x: [a for a in x.split('(')][0])
    l = list(df['Category'].unique())
    l = ['All'] + l
    return l[0], parse_options(l)

#######################################
## Update Table, Triggered by Input ###
#######################################
@app.callback (
        [Output('pg_table_article', 'data'), Output('pg_table_article', 'style_data_conditional')], 
        [Input('pg_input_dim', 'value'), Input('pg_input_cat', 'value'), Input('pg_date-picker', 'start_date'), Input('pg_date-picker', 'end_date'),
          Input('pg_input_cov', 'value'), Input('pg_input_method', 'value'), Input('pg_input_senti_w', 'value'), 
          Input('pg_input_sal_mul', 'value'), Input('pg_input_sal_filter', 'value'), Input('pg_input_senti_filter', 'value')])

def update_table(inp_dim, inp_cat, start, end, cov_in, method, senti_w, sal_w, sal_filter, senti_fil):
    df = df_input.copy()    
    df = df[df['Trust Dimension'].str.contains(inp_dim)]
    df['Category'] = df['Category'].apply(lambda x: [a for a in x.split('/')][0]).apply(lambda x: [a for a in x.split('(')][0])
    df['Trust Dimension'] = inp_dim
    
    if inp_cat == 'All':
        pass
    else:
        df = df[df['Category'].str.contains(inp_cat)]
        
    if cov_in == 'Yes':
        with_cov = True
    else:
        with_cov = False
        df['coverage'] = df['coverage_rank'].astype(float) / 10
        df['url_num'] = df.groupby(['duplicateGroupId', 'title'])['originalUrl'].transform('count')
        
    df = cal_trust_score(df, datetime.now()-pd.Timedelta(days=37), datetime.now(), w0=float(senti_w), method=method, sal_filter=float(sal_filter), 
                          up_weight=float(sal_w), senti_filter=float(senti_fil), with_rec=False, with_cov=with_cov)
    
    df['mention_ratio'] = df['brand_mentions'] / df['total_org_mentions']
    df = df[['duplicateGroupId', 'title', 'publishedDate', 'Trust Dimension', 'Category', 'Topics', 'trust_score', 'coverage', 'f_sentiment', 'f_saliency', 'mention_ratio', 'url_num', 'originalUrl']]   
    df['Topics'] = df['Topics'].str.capitalize()
    df.columns = ['GROUPID', 'TITLE', 'DATE', 'DIMENSION', 'CATEGORY', 'TOPICS', 'TRUST SCORE', 'COVERAGE', 'SENTIMENT', 'SALIENCY', 'MENTION RATIO', 'URL #', 'LINK']
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
            'maxWidth': '200px',
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