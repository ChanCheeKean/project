from dash.dependencies import Input, Output
from datetime import datetime
from app import app
from components.templates import page_1
from components.templates import page_2

### update page content with selected tab ###
@app.callback(
    Output("page_content", "children"), 
    Input("main_tab", "active_tab")
    )
def render_tab_content(tab):
    if tab == 'main_tab_a':
        return page_1.layout
    elif tab == 'main_tab_b':
        return page_2.layout
    else:
        return None