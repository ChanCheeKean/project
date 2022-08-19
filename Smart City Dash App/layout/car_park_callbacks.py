# Layout for forecasting page
from dash.dependencies import Input, Output, State
import pandas as pd
import numpy as np
from app import app
from datetime import datetime 
import calendar
import plotly.graph_objs as go
import plotly.figure_factory as ff
from utils.data_import import bg_color, txt_color, df_full

# intermediate data data
@app.callback(
        Output('carpark_intermediate', 'children'), 
        [Input('carpark_submit','n_clicks')], 
        [
         State('carpark_id_picker', 'value'),
         State('carpark_date-picker', 'start_date'), 
         State('carpark_date-picker', 'end_date')
        ])
def load_data(n_clicks, carpark_id, start, end):
    # repalce 2018 data as 2019
#    df = pd.read_csv('./data/parking.csv', index_col = 0)
    global data_full
    df = df_full.copy()
    df = df[df.index >= start.replace('2019','2018')]
    df = df[df.index < end.replace('2019','2018')]
    
#     higher rate on working day
    df['Fahrtzw'] = df.apply(lambda x:  'u' if x['Wotag'] == 6 else x['Fahrtzw'], axis = 1)
    df['parkingFacilityOccupancy'] = df.apply(lambda x:  x['parkingFacilityOccupancy']*1.8 if x['Fahrtzw'] == 'w' else x['parkingFacilityOccupancy'], axis = 1)
    df['parkingFacilityOccupancy'] = df.apply(lambda x:  x['parkingFacilityOccupancy']*1.1 if x['Fahrtzw'] == 'u' else x['parkingFacilityOccupancy'], axis = 1)
    df['parkingFacilityOccupancy'] = df.apply(lambda x:  x['parkingFacilityOccupancy']*0.5 if x['Fahrtzw'] == 's' else x['parkingFacilityOccupancy'], axis = 1)

    df['parkingFacilityOccupancy'] = df.apply(lambda x:  1 if x['parkingFacilityOccupancy'] >= 1 else x['parkingFacilityOccupancy'], axis = 1)
    df['totalNumberOfOccupiedParkingSpaces'] = df['parkingFacilityOccupancy'] * 500

#    columns = ['totalNumberOfOccupiedParkingSpaces', 'parkingFacilityOccupancy', 'Fahrtzw']
#    df[columns].to_csv('./data/parking.csv')
    return df.to_json()

# heatmap
@app.callback (
        Output('parking_hm', 'figure'),  
        [Input('carpark_intermediate', 'children')],
        )
def update_heatmap (json_data):
        # load data from intermediate
        df_filter = pd.read_json(json_data)        
        dh = df_filter.pivot_table(columns= df_filter.index.hour, 
                                  index= df_filter.index.dayofweek, 
                                  values = 'totalNumberOfOccupiedParkingSpaces')     
        # plotting
        hovertemplate = "<b> %{y}  %{x} <br><br> %{z} Occupied Parking Spaces"
        fig = ff.create_annotated_heatmap(
                            y= [calendar.day_name[a] for a in dh.index], 
                            x = [datetime.strptime(str(a), "%H").strftime("%I %p") for a in dh.columns], 
                            z = dh.astype(int).values, 
                            showscale = False,
                            name = '',
                            hovertemplate = hovertemplate,
                            colorscale= [[0, "#caf3ff"], [1, "#2c82ff"]],
                            )
        fig['layout'].update(
                font = dict(size = 10, color = txt_color),
                plot_bgcolor = bg_color, paper_bgcolor = bg_color,
                margin=dict(l=80, b=20, t=50, r=20),
                modebar={"orientation": "v"},
                xaxis=dict(
                        side="top",
                        ticks="",
                        ticklen=2,
                        tickcolor="#ffffff"
                        ),
                yaxis=dict(side="left", ticks="",),
                hovermode="closest",
                showlegend=False,)
    
        return fig

## Parking Occupancy
@app.callback (
        [Output('park_work_bar', 'value'), Output('park_school_bar', 'value'), Output('park_hol_bar', 'value')], 
        [Input('carpark_intermediate', 'children')],)

def update_occupancy_bar(json_data):
     # load data from intermediate
     df_filter = pd.read_json(json_data)
     work_occupancy = df_filter[df_filter.Fahrtzw == 'w']['parkingFacilityOccupancy'].mean()*10
     school_occupancy = df_filter[df_filter.Fahrtzw == 'u']['parkingFacilityOccupancy'].mean()*10
     sun_occupancy = df_filter[df_filter.Fahrtzw == 's']['parkingFacilityOccupancy'].mean()*10
     return work_occupancy, school_occupancy, sun_occupancy