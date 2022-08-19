# Layout for forecasting page
from dash.dependencies import Input, Output, State
from app import app
import pandas as pd
import plotly.graph_objs as go
import calendar
import plotly.figure_factory as ff
from utils.data_import import bg_color, txt_color, color_list, df_full

# generate ts plot
@app.callback(Output('da_avg_tsplot', 'figure'),
              [Input('da_intermediate', 'children'), Input('da_tabs','value')])
def update_tsplot(json_data, tab):
    global df_full
    # change historical data to current data, 2019
    df = df_full.copy()
    # higher rate on working day
    df['Fahrtzw'] = df.apply(lambda x:  'u' if x['Wotag'] == 6 else x['Fahrtzw'], axis = 1)
    df['parkingFacilityOccupancy'] = df.apply(lambda x:  x['parkingFacilityOccupancy']*1.8 if x['Fahrtzw'] == 'w' else x['parkingFacilityOccupancy'], axis = 1)
    df['parkingFacilityOccupancy'] = df.apply(lambda x:  x['parkingFacilityOccupancy']*1.1 if x['Fahrtzw'] == 'u' else x['parkingFacilityOccupancy'], axis = 1)
    df['parkingFacilityOccupancy'] = df.apply(lambda x:  x['parkingFacilityOccupancy']*0.5 if x['Fahrtzw'] == 's' else x['parkingFacilityOccupancy'], axis = 1)
    
    df.index = df.index.map( lambda x : x.replace(year = 2019))
    # resample to hour,day,month according to selected tab
    if tab == 'hour':
        df = df.groupby(df.index.hour).mean()
        df_traffic = pd.read_csv('./data/traffic_hour.csv', index_col = 0)
        
    elif tab == 'day':
        df = df.groupby(df.index.dayofweek).mean()
        df.index = [calendar.day_abbr[i] for i in df.index.values]
        df_traffic = pd.read_csv('./data/traffic_day.csv', index_col = 0)

    else:
        df = df.groupby(df.index.month).mean()
        df.index = [calendar.month_abbr[i] for i in df.index.values]
        df_traffic = pd.read_csv('./data/traffic_month.csv', index_col = 0)
        df_traffic.index = [calendar.month_abbr[i] for i in df_traffic.index.values]
 
    # categories data
    df_traffic.columns = ['Total Vehicles R1','Total Vehicles R2']
    df_env = df['no2']
    df_parking = df['parkingFacilityOccupancy']
                                   
    # plotting
    data = [
            go.Scattergl(
                    x = df_traffic.index, 
                    y = df_traffic[name],
                    mode = 'markers+lines', 
                    marker = dict(size = 8),
                    line = dict(width = 2),
                    name = name,)
            for name in df_traffic.columns]
                
    data.append(go.Scattergl(
                         x = df_env.index, 
                         y = df_env.values,
                         mode = 'markers+lines', 
                         marker = dict(size = 8, color = color_list[0]),
                         line = dict(width = 2, color = color_list[0]),
                         name = 'No2',
                         yaxis = "y2", 
                        ))
    
    data.append(go.Scattergl(
                         x = df_parking.index, 
                         y = df_parking.values,
                         mode = 'markers+lines', 
                         marker = dict(size = 8, color = color_list[1]),
                         line = dict(width = 2, color = color_list[1]),
                         name = 'Parking Occupancy',
                         yaxis = "y3", 
                        ))
    
    layout = go.Layout (
            legend_orientation="h",
            legend = dict(x = 0, y = 1.2,),
            font = dict(size = 8, color = txt_color),
            plot_bgcolor = bg_color, paper_bgcolor = bg_color,
            hovermode = 'x',
            dragmode = 'zoom', 
            showlegend = True,
            margin = dict(l = 60, r = 20, t = 25, b = 30),
            xaxis = dict(dtick = 1),
            yaxis = dict(tickformat = '.1f', domain=[0, 0.3], title = 'Traffic #', titlefont = dict(color = 'yellow')), 
            yaxis2 = dict(domain=[0.33, 0.6], title = 'No2 Volume', titlefont = dict(color = 'yellow')),
            yaxis3 = dict(domain=[0.66, 1], title = 'P Occupancy', titlefont = dict(color = 'yellow')),
            barmode='stack'
            )

    fig = go.Figure (data = data, layout = layout)

    return fig

# generate heatmap
@app.callback(Output('da_corr_hm', 'figure'),
              [Input('da_intermediate', 'children')])
def update_corr_heatmap(json_data):
    global df_full
    df = df_full[['KFZ_R1', 'KFZ_R2', 'no2', 'parkingFacilityOccupancy']].copy()
    df.columns = ['#Vehicle_R1','#Vehicle_R2','No2 Volume',' P Occupancy']
    df = df.corr()
    
    fig = ff.create_annotated_heatmap(
            z = df.values.round(2), 
            x = df.columns.tolist(), 
            y = df.index.tolist(), 
            colorscale='Reds', 
            showscale = True,
            )
    fig['layout'].update(
            margin = dict(l = 70, r = 20, t = 30, b = 20), 
            font = dict(size = 8, color = txt_color),
            plot_bgcolor = bg_color, paper_bgcolor = bg_color,
            )
    return fig
