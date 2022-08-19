from app import app
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px

df = pd.read_csv('https://plotly.github.io/datasets/country_indicators.csv')

### update options list in the dropdown
@app.callback(
    [
        Output('xaxis-column', 'options'),
        Output('xaxis-column', 'value'),
        Output('yaxis-column', 'options'),
        Output('yaxis-column', 'value'),
    ],
    Input('main_tab', 'value')
    )
    
def update_dropdown_options(_):
    option_list = df['Indicator Name'].unique()
    return option_list, option_list[0], option_list, option_list[-1]
    
    
### update plot based on dropdown selection
@app.callback(
    Output('indicator-graphic', 'figure'),
    Input('xaxis-column', 'value'),
    Input('yaxis-column', 'value'),
    )
    
def update_graph(x_axis, y_axis):
    dff = df.copy()
    
    fig = px.scatter(x=dff[dff['Indicator Name'] == x_axis]['Value'],
                     y=dff[dff['Indicator Name'] == y_axis]['Value'],
                     hover_name=dff[dff['Indicator Name'] == y_axis]['Country Name'])

    # modify 
    fig.update_layout(
        margin={'l': 40, 'b': 40, 't': 10, 'r': 0}, 
        hovermode='closest')
        
    fig.update_xaxes(title=x_axis)
    fig.update_yaxes(title=y_axis)

    return fig