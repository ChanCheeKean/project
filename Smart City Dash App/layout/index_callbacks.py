# Layout for forecasting page
from dash.dependencies import Input, Output, State
from datetime import datetime
from app import app
from utils.data_import import timezone
import dash

count = 8
# to return classname when the tab is selected
@app.callback(
    [Output(f"tab{i}", "className") for i in range(1, count)],
    [Input(f"tab{i}", "n_clicks") for i in range(1, count)],
)
def set_active(*args):
    ctx = dash.callback_context
    
    # nothing happen when no selected class
    if not ctx.triggered or not any(args):
        return ["is_activated" if f"tab{i}" == "tab1" else "tab_item" for i in range(1, count)]
            
    # get id of triggering button
    button_id = ctx.triggered[0]["prop_id"].split(".")[0]

    return [
        "is_activated" if button_id == f"tab{i}" else "tab_item" for i in range(1, count)
    ]

# update current time instantly 
@app.callback(
    [Output("current_date", "children"), Output("current_time", "children"),],
    [Input("clock_interval", "n_intervals")],
)
def update_time(n):
    return datetime.now().strftime("%Y-%m-%d"), datetime.now(timezone).strftime("%H:%M")
