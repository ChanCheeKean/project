from app import app, server
from components.templates import main, playground_layout
import dash_auth
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output

app.title = 'Edelman DXI'

############
### Auth ###
############
auth = dash_auth.BasicAuth(
    app,
    {"Edelman" : "Ed3lm@n!"})

app.layout = html.Div([
        dcc.Location(id="url"),
        html.Div(id='route_content')])

# routing
@app.callback(Output("route_content", "children"), [Input("url", "pathname")])
def render_page_content(pathname):
    if pathname == '/':
        return main.layout
    elif pathname == '/playground':
        return playground_layout.layout

if __name__ == '__main__':
    app.run_server(debug=False, port=8050)