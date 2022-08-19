import numpy as np
import pandas as pd
from dash.dependencies import Input, Output, State
from datetime import datetime
from app import app
import plotly.graph_objs as go
from plotly.subplots import make_subplots
import time
import calendar
import dash_html_components as html
from utils.data_import import bg_color, txt_color

'''
Temporary Solution to boast performance by 
pre-processing data into hourly, daily and monthly data
'''

# global counter
counter = 0

# import data
@app.callback(
        Output('traffic_intermediate', 'children'), 
        [Input('test', 'children')])
def load_data(tab):
#    global data_full
#    df = df_full.copy()
#    return df.to_json()
    return []
    
# generate ts plot for traffic volume
@app.callback(
        Output('traffic_ts_plot', 'figure'),
        [Input('trafficv_tabs', 'value'), Input('traffic_intermediate', 'children')],
)
def update_tsplot(tab_time, json_data):
#    df_filter = pd.read_json(json_data)
#    df = df_filter[['KFZ_R1', 'KFZ_R2']].copy() 
            
    if tab_time == 'm':
#        df = df.groupby(df.index.month).sum().astype(int)
#        df.index = [calendar.month_abbr[i] for i in df.index.values]
#        df.to_csv('./data/traffic_month')
        df = pd.read_csv('./data/traffic_month.csv', index_col = 0)

    elif tab_time == 'h':
#         df = df.groupby(df.index.hour).mean().astype(int)
#         df.to_csv('./data/traffic_hour.csv')
         df = pd.read_csv('./data/traffic_hour.csv', index_col = 0)
         
    else:
#        df = (df.groupby(df.index.dayofweek).sum()/52).astype(int)
#        df.index = [calendar.day_abbr[i] for i in df.index.values]
#        df.to_csv('./data/traffic_day.csv')
        df = pd.read_csv('./data/traffic_day.csv', index_col = 0)
    
    df.columns = ['Total_Vehicle_R1','Total_Vehicle_R2']

    data = [go.Scattergl(
                         x = df.index, 
                         y = df[name].values,
                         mode = 'markers+lines', 
                         marker = dict(size =6),
                         line = dict(width = 2),
                         name = name,
                        ) for i, name in enumerate(df.columns)]
                
    layout = go.Layout (
            font = dict(size = 10, color = 'white'),
            legend_orientation="h",
            plot_bgcolor = bg_color, paper_bgcolor = bg_color,
            hovermode = 'x',
            dragmode = 'zoom', 
            showlegend = True,
            yaxis = dict(title = '', titlefont = dict(color = '#0e4886'), tickformat = '.d', gridcolor='white', ticklen=5,), 
            xaxis = dict(dtick = 1),
            legend = dict(x = 0, y = 1.3, font = dict(size = 8)),
            margin = dict(l = 55, r = 20, t = 25, b = 50))

    fig_ts = go.Figure (data = data, layout = layout)
    return fig_ts
    
# generate bar chart
@app.callback (
        Output('sensor_bar_plot', 'figure'), 
        [Input('traffic_intermediate', 'children')])
def generate_barchart(json_data):
    try:
        global count
#        df_filter = pd.read_json(json_data)
        d1 = pd.DataFrame(columns = ['Cars','Bikes','Buses', 'Trucks'])
        d2 = pd.DataFrame(columns = ['Cars','Bikes','Buses', 'Trucks'])
        now = datetime.now().strftime('%H:%M:%S')
         
        d1.loc[now] = [np.random.randint(4,10), np.random.randint(1,3), np.random.randint(0,2), np.random.randint(0,2)]
        d2.loc[now] =  [np.random.randint(3,9),np.random.randint(1,4), np.random.randint(0,2), np.random.randint(0,2)] 
            
#        df_filter[['Lkw_R1','Pkw_R1', 'Mot_R1']].iloc[count,:]
#        d1.index = ['Truck','Car','Bike']
#        d2 = df_filter[['Lkw_R2','Pkw_R2', 'Mot_R2']].iloc[count,:]
#        d2.index = ['Truck','Car','Bike']
        
        data = [
                go.Bar(
                x = d1.values.tolist()[-1], 
                y = d1.columns, 
                orientation='h',
                name = 'From Town'),
                        
                go.Bar(
                x = d2.values.tolist()[-1], 
                y = d2.columns, 
                orientation='h',
                name = 'To Town')]
        
        layout = go.Layout (
                showlegend = True,
                plot_bgcolor = bg_color, paper_bgcolor = bg_color,
                legend_orientation="h",
                legend = dict(x = 0.5, y = -0.1, font = dict(size = 10)),
                yaxis = dict(ticklen=5, ),
#                xaxis = dict (range=[0, 15]),
                font = dict(size = 10, color = txt_color), 
                margin = dict(l = 50, r = 20, t = 30, b = 30),
                )
        fig = go.Figure (data = data, layout = layout)    
        return fig

    except:
        return []

# generate pie chart
@app.callback (Output('traffic_pie_chart', 'figure'), [Input('traffic_intermediate', 'children'),])
def update_pie_chart (json_data):
        # load data from intermediate
#        df_filter = pd.read_json(json_data)
#        d1 = df_filter[['Lkw_R1','Pkw_R1', 'Mot_R1']].sum()
#        d1.index = ['Truck','Car','Bike']
#        d2 = df_filter[['Lkw_R2','Pkw_R2', 'Mot_R2']].sum()
#        d2.index = ['Truck','Car','Bike']
#        df = pd.concat([d1.rename('d1'),d2.rename('d2')],axis = 1)
#        df.to_csv('./data/traffic_sum.csv')
        df = pd.read_csv('./data/traffic_sum.csv', index_col = 0)
        
        fig = make_subplots(rows=1, cols=2, specs=[[{'type':'domain'}, {'type':'domain'}]])
        
        fig.add_trace(
                go.Pie(labels = df['d1'].index.values, 
                        values = df['d1'].values, 
                        name = '',
                        hole=.5),
                1, 1)
        
        fig.add_trace(
                go.Pie(labels = df['d2'].index.values , 
                        values = df['d2'].values, 
                        name = '',
                        hole=.5),
                1, 2)
                
        fig['layout'].update(
            legend_orientation="h",
            legend = dict(x = 0, y = 1.5, font = dict(size = 8)),
            margin=dict(l = 20, b = 5, t = 40, r = 10),
            font = dict(size = 10, color = 'white'),
            plot_bgcolor = bg_color, paper_bgcolor = bg_color,
            annotations=[
                    dict(text='Toward', x=0.14, y=0.5, font_size= 10, showarrow=False),
                    dict(text='From', x=0.86, y=0.5, font_size = 10, showarrow=False)])
        return fig

# generate random speed
@app.callback (Output('avg_speed', 'children'), 
               [Input('traffic_intermediate', 'children')])
def update_speed(json_data):
    rand = np.round(np.random.uniform(42,48),2)
    return f'{rand} km/h'

# collapse alert
@app.callback(
    Output("collision_collapse", "is_open"),
    [Input("collision_button", "n_clicks")],
    [State("collision_collapse", "is_open")],
)
def toggle_collision_collapse(n, is_open):
    if n:
        return not is_open
    return is_open

@app.callback(
    Output("rb_collapse", "is_open"),
    [Input("rb_button", "n_clicks")],
    [State("rb_collapse", "is_open")],
)
def toggle_roadblock_collapse(n, is_open):
    if n:
        return not is_open
    return is_open

@app.callback(
    Output("congestion_collapse", "is_open"),
    [Input("congestion_button", "n_clicks")],
    [State("congestion_collapse", "is_open")],
)
def toggle_congestion_collapse(n, is_open):
    if n:
        return not is_open
    return is_open

# collapse/expand tree chart
@app.callback(
    Output("traffic_tree_collapse", "is_open"),
    [Input("traffic_tree_button", "n_clicks")],
    [State("traffic_tree_collapse", "is_open")],
)
def toggle_tree_button_collapse(n, is_open):
    if n:
        return not is_open
    return is_open

# image/video for tab
@app.callback(
    Output("spot_content", "children"),
    [Input("traffic_tabs", "value"), Input('traffic_interval','n_intervals')],
)
def change_spot_content(tab, n):
    global counter
    
    # reset counter to 0
    if counter >= 17:
        counter = 0
        
    if tab == 'a':
        return html.Video(src = '/static/sample_with_count.webm', style=dict(height = '350px', width = '100%'), loop = True, autoPlay = True)

    elif tab == 'b':
        img = "./static/spotb.png"
        return html.Img(src = img, style=dict(height = '350px', width = '100%'), )

    elif tab == 'c':
#        img = f"https://www.schwaebisch-gmuend.de/files/upload/webcam/marktplatz1/gmuendcam.jpg?rnd={time.time()}"
        counter = counter+ 1
        img = f'./static/img/market/{counter}market_out.jpg'
        return html.Img(src = img, style=dict(height = '350px', width = '100%'), )
    
    elif tab == 'd':
#        img = f"https://www.schwaebisch-gmuend.de/webcam_ropa.php?image=weleda.jpg&rnd={time.time()}"
        counter = counter + 1
        img = f'./static/img/tunnel/{counter}tunnel_out.jpg'
        return html.Img(src = img, style=dict(height = '350px', width = '100%'), )