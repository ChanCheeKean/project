# Layout for forecasting page
from dash.dependencies import Input, Output
import dash_html_components as html
from datetime import datetime
import dash_bootstrap_components as dbc
from app import app
from components.templates import page1_layout, page2_layout, page3_layout

#################################################
### Update Current, Triggered Every n seconds ###
#################################################
@app.callback(
    [Output("current_date", "children"), Output("current_time", "children"),],
    [Input("clock_interval_30", "n_intervals")],
)
def update_time(n):
    return datetime.now().strftime("%Y-%m-%d"), datetime.now().strftime("%H:%M")

#############################################
### Update Page Content, Triggered by Tab ###
#############################################
@app.callback(Output("page_content", "children"), [Input("main_tab", "active_tab")])
def render_tab_content(tab):
    if tab == 'main_tab_a':
        return page1_layout.layout
    elif tab == 'main_tab_b':
        return page2_layout.layout
    elif tab == 'main_tab_c':
        return page3_layout.layout
    else:
        return None
