# Layout for forecasting page
import pandas as pd
import numpy as np
from dash.dependencies import Input, Output, State
from utils.plot_helper import get_radar_plot
from app import app
import io, base64
from utils.data_loader import fetch_data, cal_trust_score
from datetime import datetime

# load real data
path = './data/LN_amazon_processed_50k.pkl'
df_input = fetch_data(path, start=datetime.now()-pd.Timedelta(days=7), end=datetime.now())

####################################################
### Parse Uploaded Excel, Triggered by Uploading ###
####################################################

# function for parsing
def parse_contents(contents, filename):
    content_type, content_string = contents.split(',')
    decoded = base64.b64decode(content_string)
    try:
        if 'csv' in filename:
            # Assume that the user uploaded a CSV file
            df = pd.read_csv(io.StringIO(decoded.decode('utf-8')))
        elif 'xls' in filename:
            # Assume that the user uploaded an excel file
            df = pd.read_excel(io.BytesIO(decoded))
        return df
    except Exception as e:
        print(e)

@app.callback (
        Output('trading_intermediate', 'children'),
        [Input('upload-data', 'contents')],
        [State('upload-data', 'filename')]
)
def upload_data(content, filename):
    if content is not None:
        print(filename)
        df = parse_contents(content, filename)
        return df.to_json()
    else:
        return None

##########################################
### Update Data, Triggered by Dropdown ###
##########################################

# @app.callback (
#         [Output('input_isin', 'value'), Output('input_bond', 'value'), 
#          Output('input_issuer', 'value'), Output('trading_intermediate_2', 'children')],
#         [Input('input_submit', 'n_clicks'), Input('trading_intermediate', 'children'), ],
#         [State('input_isin', 'value'), State('input_bond', 'value')]
# )
# def update_bond(_, json_data, isin, bond):
#     df = pd.read_json(json_data)
    
#     if (isin is not None) & (isin != 'Not Found'):
#         # if filling isin
#         df = df[df['ISIN CODE'] == isin]
        
#         if len(df):
#             return isin, df['INST_SH_NAM'].unique()[0], 'Not Found', df.to_json()
#         else:
#             return 'Not Found', 'Not Found', 'Not Found', None

#     else:
#         # if filling bond
#         df = df[df['INST_SH_NAM'] == bond]
#         if len(df):
#             return df['ISIN CODE'].unique()[0], bond, 'Not Found', df.to_json()
#         else:
#             return 'Not Found', 'Not Found', 'Not Found', None

###############################################
### Update table, Triggered by Updated Data ###
###############################################
# @app.callback (
#         [Output('count_table', 'data'), Output('latest_table', 'data')],
#         [Input('trading_intermediate_2', 'children')],
# )
# def update_count_table(json_data):
#     # df_foo = df.copy()
#     if json_data is not None:
#         df_foo = pd.read_json(json_data)
#         df_bar = df_foo.groupby('BROKER')[['BROKER_INIT']].count().head(10).reset_index().sort_values('BROKER_INIT', ascending=False)
#         df_bar.columns = ['BROKERS', 'COUNTS']
#         df_boo = df_foo.sort_values(['XACT_DAT']).tail(10).sort_values('XACT_DAT', ascending=False)
#         df_boo = df_boo[['XACT_DAT', 'INST_QTY', 'XACT_SIGN', 'INST_PRICE']]
#         df_boo.columns = ['Date' , 'Size', 'Side', 'Price']
        
#         return df_bar.to_dict('records'), df_boo.to_dict('records')
#     else:
#         return pd.DataFrame().to_dict('records'), pd.DataFrame().to_dict('records')
        
#######################################################
### Collapsible Image, Triggered by CLicking BUtton ###
#######################################################
# @app.callback(
#     Output("story_collapse", "is_open"),
#     [Input("story_button", "n_clicks")],
#     [State("story_collapse", "is_open")],
# )
# def toggle_tree_collapse(n, is_open):
#     if n:
#         return not is_open
#     return is_open
    
###################################################
### Update Radar, Triggered by User Input Group ###
###################################################
@app.callback (
        Output('pg1_radar', 'figure'),
        [Input('input_brand', 'value'), Input('input_country', 'value'),]
)

def update_radar(inp_brand, inp_country):
    
    df = df_input.copy()       
    lis = []
    for dim in ['Ability', 'Integrity', 'Purpose', 'Dependability']:
        foo = df[df['Trust Dimension'].str.contains(dim)].copy()
        foo['Trust Dimension'] = dim
        foo = cal_trust_score(foo, datetime.now()-pd.Timedelta(days=7), datetime.now(), w0=0.8, with_rec=True)         
        lis.append(foo)
    df = pd.concat(lis)
    
    df = df[['Trust Dimension', 'trust_score']]
    df.columns=['Dimension', 'Trust Score']
    df['brand'] = inp_brand    
    df = df.groupby(['brand', 'Dimension']).sum().unstack().reset_index().set_index('brand')
    df.columns = [x[1] for x in df.columns]
    df['self'] = 10
    df.loc['Industry BenchMark'] = [-10, -10, -10, -10, -10]
    df = (df / 10).round(2)
    return get_radar_plot(df, [-10, 10], height=275)

###################################################
### Update Table, Triggered by User Input Group ###
###################################################
@app.callback (
        [Output('table_1', 'data'), Output('table_1', 'style_data_conditional')], 
        [Input('input_brand', 'value'), Input('input_dim_pg1', 'value'), Input('input_country', 'value'),]
)
def update_table(inp_brand, inp_trust, inp_country):
    
    dic = {}
    for p in ['Ability', 'Dependability', 'Integrity', 'Purpose']:
        foo = pd.DataFrame(np.random.randint(40, 100, (6, 1)),
                            index=['Amazon', 'Facebook', 'AstraZeneca', 'Shell', 'Unilever', 'Google'], 
                            columns=['SCORES']).reset_index().rename(columns={'index': 'BRANDS'})
        
        foo.sort_values('SCORES', inplace=True, ascending=False)
        foo['RANKS'] = range(1, foo.shape[0] + 1)
        foo['CHANGES'] = ['▲ 2', '—', '▲ 1', '▼ 2', '▲ 2', '▼ 3']
        dic[p] = foo
    try:
        dic = dic[inp_trust]
    except:
        dic = dic['Ability']
    
    style = [
        {
            'if': {'filter_query': '{{BRANDS}} = {}'.format(inp_brand)},
            'border': 'none',
            'color': 'rgb(51, 204, 204)',
            'fontWeight': 'bold',
            'fontSize': '16px',
            },
        
        {
            'if': {'column_id': ['RANKS', 'SCORES', 'BRANDS']},
            'borderRight' : '1px solid white',
            },
        
        {
            'if': {'filter_query': '{CHANGES} contains "▼"', 'column_id': 'CHANGES'},
            'color': 'red',
            },
        
         {
            'if': {'filter_query': '{CHANGES} contains "—"', 'column_id': 'CHANGES'},
            'color': 'white',
            },
        
                {
        'if': {'filter_query': '{CHANGES} contains "▲"', 'column_id': 'CHANGES'},
            'color': 'rgb(51, 204, 204)',
            },
        
        {
            "if": {"state": "active"}, 
            "backgroundColor": "inherit !important", 
            "border": "none !important"
            },
      ]
    
    return dic.to_dict('records'), style

# @app.callback (
#         [Output('ability_table', 'data'), Output('dependability_table', 'data'), Output('integrity_table', 'data'), Output('purpose_table', 'data'),
#          Output('ability_table', 'style_data_conditional'), Output('dependability_table', 'style_data_conditional'), 
#          Output('integrity_table', 'style_data_conditional'), Output('purpose_table', 'style_data_conditional')], 
#         [Input('input_brand', 'value')]
# )
# def update_table(inp_brand):
    
#     dic = {}
#     for p in ['A', 'D', 'I', 'P']:
#         foo = pd.DataFrame(np.random.randint(40, 100, (5, 1)),
#                            index=['Amazon', 'Facebook', 'AstraZeneca', 'Shell', 'Unilever'], 
#                            columns=['SCORES']).reset_index().rename(columns={'index': 'BRANDS'})
#         foo.sort_values('SCORES', inplace=True, ascending=False)
#         foo['RANKS'] = range(1, foo.shape[0] + 1)
#         dic[p] = foo
    
#     style = [
#         {
#             'if': {'filter_query': '{{BRANDS}} = {}'.format(inp_brand)},
#             'backgroundColor': 'inherit',
#             'border': 'none',
#             'color': 'rgb(51, 204, 204)',
#             'fontWeight': 'bold',
#             'fontSize': '14px',
#             },
        
#         {
#             "if": {"state": "active"}, 
#             "backgroundColor": "inherit !important", 
#             "border": "inherit !important"
#             },
#      ]
    
#     return (dic['A'].to_dict('records'), dic['D'].to_dict('records'), dic['I'].to_dict('records'), dic['P'].to_dict('records'),
#             style, style, style, style)
    
############################################
### Update Gauge, Triggered by n seconds ###
############################################
@app.callback (
        Output('trust_gauge', 'value'), 
        [Input('clock_interval_30', 'n_intervals'),  Input('input_dim_pg1', 'value'), Input('input_brand', 'value'), Input('input_country', 'value'),]
)

def update_trust_barometer(n, inp_trust, inp_brand, inp_country):
    df = df_input.copy()   
    df = cal_trust_score(df, datetime.now()-pd.Timedelta(days=7), datetime.now(), w0=0.8, with_rec=True)['trust_score']
    return round(df.sum() , 2)