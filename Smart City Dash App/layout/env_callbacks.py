# Layout for forecasting page
from dash.dependencies import Input, Output, State
import pandas as pd
import numpy as np
from app import app
import plotly.graph_objs as go
from datetime import datetime
from utils.data_import import df_full, bg_color, txt_color, color_list, timezone

# generate selected-ts plot
@app.callback(Output('env_tsplot', 'figure'),
              [Input('env_intermediate', 'children'), Input('env_tabs','value')])
def update_tsplot(json_data, tab):
    global df_full
    # change historical data to current data, 2019 and 2020
    df = df_full[['no2']].copy()
    df_2020 = df_full[['no2']].copy()
    df.index = df.index.map( lambda x : x.replace(year = 2019))
    df_2020.index = df_2020.index.map( lambda x : x.replace(year = 2020))
    df = pd.concat([df, df_2020],axis = 0, sort = True)
    
    # hour,day,month according to selected tab
    if tab == 'hour':
        freq = '1H'
        pred_leng = 13
    elif tab == 'day':
        freq = '1D'
        pred_leng = 8
    else:
        freq = '1m'
        pred_leng = 4
    
    # resample data accotding to selected tab
    df = df.resample(freq).mean()
    df_actual = df[df.index <= datetime.now(timezone)].iloc[-6:,]
    df_predict = df[df.index > datetime.now(timezone)].iloc[:pred_leng,].rename(columns={"no2": "Forecast"})
                                       
    # set upper and lower limit
    usl = 60
    mean = df.mean().values[0]
    lsl = 5
    
    # out of limit
    d1 = df_actual[df_actual ['no2'] >= usl].rename(columns={"no2": "Out"})
    d2 = df_predict[df_predict['Forecast'] >= usl].rename(columns={"Forecast": "Out"})
    df_out = pd.concat([d1,d2], axis = 0, sort = True)
    
    # plotting
    data = [
            go.Scattergl(
                         x = df_actual.index, 
                         y = df_actual['no2'],
                         mode = 'markers+lines', 
                         marker = dict(size = 6, color = color_list[1]),
                         line = dict(width =2.5, color = color_list[1]),
                         name = 'NO2',
                        ),  
            
            go.Scattergl(
                         x = df_predict.index, 
                         y = df_predict['Forecast'],
                         mode = 'markers+lines', 
                         marker = dict(size = 6, color = color_list[0]),
                         line = dict(width =2.5, color = color_list[0]),
                         name = 'Forecasted',
                        ),            
            go.Scattergl(
                         x = df_out.index, 
                         y = df_out['Out'],
                         mode = 'markers', 
                         marker = dict(size = 10, color = "rgba(210, 77, 87, 0.7)", symbol = 'square'),
                         name = 'Out of Control',
                        ),
                        ]
                
    layout = go.Layout (
            legend_orientation="h",
            legend = dict(x = 0, y = 1.2,),
            font = dict(size = 8, color = txt_color),
            plot_bgcolor = bg_color, paper_bgcolor = bg_color,
            hovermode = 'closest',
            dragmode = 'zoom', 
            showlegend = True,
            yaxis = dict(tickformat = '.2f',), 
            margin = dict(l = 40, r = 10, t = 25, b = 40),
            )

    fig = go.Figure (data = data, layout = layout)
    
    # straight line and annotations
    fig['layout'].update(
            shapes = [
                    # Upper Limit
                    go.layout.Shape(type = 'line', xref = "x", yref = "y", x0 = df_actual.index.min(), y0 = usl, x1 = df_predict.index.max(), y1 = usl, 
                                    line = {"color": "#91dfd2", "width": 2, "dash": "dot"},),
                    # Lower Limit           
                    go.layout.Shape(type = 'line', xref = "x", yref = "y", x0 = df_actual.index.min(), y0 = lsl, x1 = df_predict.index.max(), y1 = lsl, 
                                    line = {"color": "#91dfd2", "width": 2, "dash": "dot"},),
                    #mean
                    go.layout.Shape(type = 'line', xref = "x", yref = "y", x0 = df_actual.index.min(), y0 = mean, x1 = df_predict.index.max(), y1 = mean, 
                                    line = {"color": "rgb(255,127,80)", "width": 3, "dash": "dot"},),
                    ],
            annotations=[
                    go.layout.Annotation( x = 0.5, y = lsl - 0.5, xref = "paper", yref =  "y", text = "Lower Limit:" + str(round(lsl, 2)),
                                         showarrow = False, font = {"color": "white", "size" : 12},),
                    go.layout.Annotation( x = 0.5, y = usl + 0.5, xref = "paper", yref =  "y", text = "Upper Limit:" + str(round(usl, 2)),
                                         showarrow = False, font = {"color": "white", "size" : 12},),
                    go.layout.Annotation( x = 0.5, y = mean, xref = "paper", yref =  "y", text = "Mean:" + str(round(mean, 2)),
                                         showarrow = False, font = {"color": "white", "size" : 12},)
                    ],
            )
    return fig

# update wind polar chart and gauge
@app.callback([Output('NO_gauge', 'value'), Output('PM10_gauge', 'value'), Output('PM25_gauge', 'value'), Output('wind_polar', 'figure')],
              [Input('env_intermediate', 'children'), Input('env_interval', 'n_intervals')])
def update_polarc_gauge(json_data, n):
    # plotting with static value
    
    r_rand =  np.random.uniform(2, 4)
    theta_rand = np.random.randint(0, 120)
    data = [
            go.Barpolar(
                    r=[r_rand , ],
                    theta=[theta_rand, ],
                    width=[30,],
                    marker_color=[color_list[0], ],
                    marker_line_color="black",
                    marker_line_width=2,
                    opacity=0.8)
            ]
    
    layout = go.Layout(
            font = dict(size = 10, color = txt_color),
            plot_bgcolor = bg_color, paper_bgcolor = bg_color,
            margin = dict(l = 5, r = 5, t = 20, b = 10),
            polar = dict(bgcolor = '#9e9e9e',
                         radialaxis = dict(range=[0, 5]),),
            radialaxis = dict(range=[0, 5],)
            )
    
    fig = go.Figure(data = data, layout = layout)
    return np.random.randint(70, 100), np.random.randint(40, 70), np.random.randint(80, 120), fig    