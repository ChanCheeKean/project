## Main Page
from _plotly_future_ import v4_subplots
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html
from app import app, server
from dash.dependencies import Input, Output
from layout import city_map_layout, traffic_layout, car_park_layout,  env_layout, mapTesting_layout, echarge_layout, roadworks_layout, route_layout, da_layout
from layout import city_map_callbacks, traffic_callbacks, car_park_callbacks, env_callbacks, index_callbacks, roadworks_callbacks, echarge_callbacks, da_callbacks

# set title to be displayed
app.title = 'City Management'

##################
# Side-Bar
##################
sidebar = html.Div([dbc.Nav([
                                # city
                                dbc.NavLink([
                                        html.Img(src = './static/city-icon.png', className = 'icon d-inline-block'),
                                        html.P("City Overview", className = 'd-inline-block pl-3')
                                        ],
                                        href="/", className = 'tab_item', id = 'tab1'),

                                dbc.NavLink([
                                        html.Img(src = './static/car-icon.png', className = 'icon d-inline-block'),
                                        html.P("Traffic", className = 'd-inline-block pl-3')
                                        ],
                                        href="/traffic", className = 'tab_item', id = 'tab2'),

                                dbc.NavLink([
                                        html.Img(src = './static/parking-icon.png', className = 'icon d-inline-block'),
                                        html.P("Parking Lots", className = 'd-inline-block pl-3')
                                        ],
                                        href="/parking", className = 'tab_item', id = 'tab3'),

                                dbc.NavLink([
                                        html.Img(src = './static/env-icon.png', className = 'icon d-inline-block'),
                                        html.P("Environment", className = 'd-inline-block pl-3')
                                        ],
                                        href="/env", className = 'tab_item', id = 'tab4'),

                                dbc.NavLink([
                                        html.Img(src = './static/echarge-icon.png', className = 'icon d-inline-block'),
                                        html.P("E-Charging", className = 'd-inline-block pl-3')
                                        ],
                                        href="/echarge", className = 'tab_item', id = 'tab5'),
                                
                                dbc.NavLink([
                                        html.Img(src = './static/roadblock-icon.png', className = 'icon d-inline-block'),
                                        html.P("Roadworks", className = 'd-inline-block pl-3')
                                        ],
                                        href="/roadworks", className = 'tab_item', id = 'tab6'),
                                
                                dbc.NavLink([
                                        html.Img(src = './static/analytics-icon.png', className = 'icon d-inline-block'),
                                        html.P("Data Analytics", className = 'd-inline-block pl-3')
                                        ],
                                        href="/analytic", className = 'tab_item', id = 'tab7'),

#                                dbc.NavLink([
#                                        html.Img(src = './static/env-icon.png', className = 'icon d-inline-block'),
#                                        html.P("Map(Testing)", className = 'd-inline-block pl-3')
#                                        ],
#                                        href="/map", className = 'tab_item', id = 'tab8'),
                                ],
                                vertical=True,
                                ),
                ], className = 'tab_nav')

# change count # in index_callbacks for any tabs added

##################
# Content
##################
content = html.Div([
        ], className = 'tab__content', id = 'page_content')

##################
# Datetime
##################
clock = html.Div([
        html.Span('Live Updates', className = 'text-white lead font-weight-bold'),
        html.Span(' | ', className = 'text-white lead'),
        html.Span(id = "current_date", className = 'text-white-50 lead'),
        html.Span('  ', className = 'text-white'),
        html.Span(id = "current_time", className = 'text-white-50 lead'),
        html.Span(' | ', className = 'text-white lead'),
        dbc.Button(html.Img(src = './static/refresh-icon.png', className = 'icon'), className = 'd-inline-block icon-button', outline=False)
        ], className = 'time float-right pr-3')

##################
# Main Layout
##################
app.layout = html.Div([
        dcc.Location(id="url"),
        clock,
        sidebar,
        dcc.Interval(id='clock_interval', interval=30*1000, n_intervals=0),
        content
        ],className = 'tabs--primary')

@app.callback(Output("page_content", "children"), [Input("url", "pathname")])
def render_page_content(pathname):
    if pathname == '/':
        return city_map_layout.layout

    elif pathname == "/traffic":
        return traffic_layout.layout

    elif pathname == "/parking":
        return car_park_layout.layout

    elif pathname == "/env":
        return env_layout.layout

    elif pathname == "/echarge":
        return echarge_layout.layout
    
    elif pathname == "/roadworks":
        return roadworks_layout.layout

#    elif pathname == "/map":
#        return mapTesting_layout.layout
    
    elif pathname == "/analytic":
        return da_layout.layout
    
    else:
    # If the user tries to reach a different page, return a 404 message
        return dbc.Jumbotron(
            [
                html.H1("404: Not found", className="text-danger"),
                html.Hr(),
                html.P(f"The pathname {pathname} was not recognised..."),
            ])

if __name__ == '__main__':
    app.run_server(debug=False, port=8050)