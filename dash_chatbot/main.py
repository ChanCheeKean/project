import time
from textwrap import dedent
import dash
from dash import html, dcc, Input, Output, State
import dash_bootstrap_components as dbc

### Define app ###
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server

# Authentication # 
# openai.api_key = os.getenv("OPENAI_KEY")

### header ###
header = dbc.Row([
    dbc.Col(
        html.H1("Chatbot", className='mt-2'), 
        width=8
    ), 
    # dbc.Col(
    #     html.Img(src=app.get_asset_url("logo.png"), style={"float": "right", "height": 60}), 
    #     width=4
    # )
])

### conversation layout ###
conversation = html.Div(
    html.Div(id="display-conversation"),
    style={
        "overflow-y": "auto",
        "display": "flex",
        "height": "calc(90vh - 100px)",
        "flex-direction": "column-reverse",
    },
)

###  input group ###
controls = dbc.InputGroup(
    children=[
        dbc.Input(id="user-input", placeholder="Write a message...", type="text"),
        dbc.Button("Submit", id="submit"),
    ]
)

### final layout ###
app.layout = dbc.Container(
    fluid=False,
    children=[
        header,
        html.Hr(),
        dcc.Store(id="store-conversation", data=""),
        dbc.Spinner(html.Div(id="loading-component"), size='sm', color="info"),
        conversation,
        controls,
    ],
)

### callback ###
# store conversation history #
def create_textbox(text, box="AI"):
    text = text.replace("You:", "")
    style = {
        "max-width": "60%",
        "width": "max-content",
        "padding": "1px 1px",
        "border-radius": 20,
        "margin-bottom": 10,
    }

    if box == "user":
        thumbnail = html.Img(
            src=app.get_asset_url("profile.png"),
            style={
                "border-radius": 50,
                "height": 36,
                "margin-left": 5,
                "float": "right",
            },
        )
        style["margin-left"] = "auto"
        style["margin-right"] = 0
        textbox = dbc.Card(text, style=style, body=True, color="primary", inverse=True)
        return html.Div([thumbnail, textbox])

    elif box == "AI":
        style["margin-left"] = 0
        style["margin-right"] = "auto"
        thumbnail = html.Img(
            src=app.get_asset_url("profile.png"),
            style={
                "border-radius": 50,
                "height": 36,
                "margin-right": 5,
                "float": "left",
            },
        )
        textbox = dbc.Card(text, style=style, body=True, color="light", inverse=False)
        return html.Div([thumbnail, textbox])

    else:
        raise ValueError("Incorrect option for `box`.")

# display conversation history #
@app.callback(
    Output("display-conversation", "children"), 
    [Input("store-conversation", "data")]
)
def update_display(chat_history):
    return [
        create_textbox(x, box="user") if i % 2 == 0 else create_textbox(x, box="AI")
        for i, x in enumerate(chat_history.split("<split>")[:-1])
    ]

# clear user input after submit #
@app.callback(
    Output("user-input", "value"),
    [Input("submit", "n_clicks"), Input("user-input", "n_submit")],
)
def clear_input(n_clicks, n_submit):
    return ""

# store user input in history #
description = """
You are a friendly AI.
"""
@app.callback(
    [Output("store-conversation", "data"), Output("loading-component", "children")],
    [Input("submit", "n_clicks"), Input("user-input", "n_submit")],
    [State("user-input", "value"), State("store-conversation", "data")],
)
def run_chatbot(n_clicks, n_submit, user_input, chat_history):
    # prevent initial loading
    if n_clicks == 0 and n_submit is None:
        return "", None

    if user_input is None or user_input == "":
        return chat_history, None

    prompt = dedent(
        f"""
    {description}

    AI: Hello!
    User: Hello! Glad to be talking to you today.
    """
    )

    # First add the user input to the chat history
    chat_history += f"You: {user_input}<split>User:"
    model_input = prompt + chat_history.replace("<split>", "\n")
    # response = openai.Completion.create(
    #     engine="davinci",
    #     prompt=model_input,
    #     max_tokens=250,
    #     stop=["You:"],
    #     temperature=0.9,
    # )
    # model_output = response.choices[0].text.strip()
    model_output = "AI Generated Output"
    chat_history += f"{model_output}<split>"
    time.sleep(0.5)
    return chat_history, None

if __name__ == "__main__":
    app.run_server(debug=False, port='8050')