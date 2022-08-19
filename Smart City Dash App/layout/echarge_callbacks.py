# Layout for forecasting page
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import dash_daq as daq
import pandas as pd
import numpy as np
import random
from app import app
import plotly.graph_objs as go
from datetime import datetime
from utils.data_import import bg_color, txt_color, color_list
from data.bingmaps_data import pp_echarging

count = 1

# to return details according to selectedpushpin
@app.callback(
     [Output('ev_img', 'src'), Output('ev_name', 'children'),
      Output('ev_station', 'children'),Output('hour_info', 'children'),
      Output('payment_info', 'children'), Output('operator_info', 'children'),
      Output('review_info', 'children'), 
      ],
     [Input('ev_map', 'selected')])
def update_details(selected):
    global count 
    count = (count%3) + 1
    
    if selected == None:
        selected_pp = pp_echarging[0]
    else:
        selected_pp = [p for p in  pp_echarging if p['metadata']['id'] == selected][0]
        
    ev_img = f'./static/EV-Station-{count}.jpg'
    ev_name = selected_pp['metadata']['address']
    ev_station = selected_pp['metadata']['title']
    hour_info = selected_pp['metadata']['hours']
    payment_info = selected_pp['metadata']['access']
    operator_info = selected_pp['metadata']['operator']
    review_info = str(round(np.random.uniform(3.5,4.8),2)) + '/5'
    
    return ev_img, ev_name, ev_station, hour_info, payment_info, operator_info, review_info

# station table
@app.callback (
        Output('ev_table_body', 'children'),
        [Input('ev_map', 'selected')],)
def update_price_plot (selected):
    
    if selected == None:
        return []
    else:
        selected_pp = [p for p in  pp_echarging if p['metadata']['id'] == selected][0]
        
    outlet_list = (selected_pp['metadata']['outlets'] + ', ').split('),')[:-1]
    row_list = []
    
    for i, outlet in enumerate(outlet_list):  
        # random number of occupancy
        outlet_count =  int(outlet.split('x ')[0])   
        if outlet_count == 1:
            bar_value = random.choice([0,10]) 
        elif outlet_count == 2:
            bar_value = random.choice([0, 5, 10]) 
        elif outlet_count == 3:
            bar_value = random.choice([0, 6.5, 10]) 
        else:
            bar_value = [9]
                    
        bar = daq.GraduatedBar(
                value = bar_value,
                max = 10,
                size = 100,
                labelPosition = 'bottom',
                color={"ranges": {"#05f7cf": [0, 3], "#f4d44d": [3, 7], "#f45060": [7, 10],},},
                )  
        
        row = html.Tr([
            html.Td(children = str(outlet.split('x ')[-1]) + ')'), 
            html.Td(html.P(str(outlet_count))),
            html.Td(html.P([np.random.randint(30,45), ' mins'])),
            html.Td(bar),
            html.Td(dcc.Graph (figure = price_plot(), style=dict(height = '35px',)), style=dict(width = '30%',)),
            ], className = 'echarge_table_row')
        
        row_list.append(row)

    return row_list

def price_plot():
    date_rng = pd.date_range(end = datetime.now(), periods = 10,  freq = '1D').strftime("%d/%b")
    df = pd.DataFrame(
            index = date_rng,
            data = {
                    'Price' : abs(np.random.normal(1.2,1,size=(len(date_rng))))
            })
    
    data = go.Scattergl( 
            x = df.index,
            y = df['Price'].round(3), 
            hovertemplate = "<b> %{x} € %{y}/L",
            name = '',
            mode = 'markers+lines', 
            hoverinfo="text",
            marker = dict(size = 6, color = color_list[0]))
        
    layout = go.Layout (
            hovermode = 'x',
            showlegend = False,
            font = dict(size = 10, color = txt_color),
            plot_bgcolor = bg_color, paper_bgcolor = bg_color,
            xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
            yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
            margin = dict(l = 5, r = 5, t = 5, b = 5))
    fig = go.Figure (data = [data], layout = layout)
    return fig