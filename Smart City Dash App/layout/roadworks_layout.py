import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import dash_table as dtb
import dash_daq as daq
from datetime import datetime, timedelta
from utils.dash_helpers import parse_options
import pandas as pd
import bing_maps_smartcity as bms
from data.bingmaps_data import pp_roadworks, pl_roadworks

##################
# Row 0 - Functionality Tree
##################
func_tree = html.Div([
                    dbc.Button([
                            html.Img(src = './static/down-icon.png', className = 'icon d-inline-block mb-1', ),
                            ], id = 'roadworks_tree_button', outline=False, className = 'tree_button'),
                    dbc.Collapse([
                            dbc.Card([
                                    dbc.CardHeader('Functionality Tree', className = 'card_header'),
                                    html.Img(src='./static/Showcase UI Roadworks.jpg', style=dict(height = '500px')),
                                    ], className = 'card py-2')
                            ],id="roadworks_tree_collapse",)])

##################
# Roadwork Map
##################
bing_map = dbc.Card([
            dbc.CardHeader('Roadwork Map', className = 'card_header'),
            bms.BingMaps(
                id = 'roadwork_map',
                polylines = pl_roadworks,
                pushpins = pp_roadworks,
                )
            ], className = 'card', style={'height': '400px'})

##################
# Roadwork Details
##################
rwd_header = dbc.Row([
                dbc.Col(html.Img(src='./static/roadworksSign_details.png', className = 'rw_icon', style={'verticalAlign': 'middle'}), width = 4, style= {'textAlign': 'center'}),
                dbc.Col([
                    html.P('Select pushpin/table entry to view the details', id='rwd_header', className='detail_head'),
                    html.P(id='rwd_id'),
                ], width=8)
            ])
rwd_schedule = html.Div([
                dbc.Row([
                    dbc.Col(html.P('Started', className='detail_title'), width = 5),
                    dbc.Col([html.P('-', id='rwd_start',  className='detail_info')], width = 7),
                ]),
                dbc.Row([
                    dbc.Col(html.P('Due Date', className='detail_title'), width = 5),
                    dbc.Col([html.P('-', id='rwd_end',  className='detail_info')], width = 7),
                ]),
                dbc.Row([
                    dbc.Col(html.P('Est. Completion', className='detail_title'), width = 5),
                    dbc.Col([html.P('-', id='rwd_est',  className='detail_info')], width = 7),
                ], id = 'rwd_est_div')
            ])
rwd_location = dbc.Row([
                    dbc.Col(html.P('Location', className='detail_title'), width = 5),
                    dbc.Col([html.P('-', id='rwd_loc',  className='detail_info')], width = 7),
                ])
rwd_obstractions = html.Div([
                dbc.Row([
                    dbc.Col(html.P('Speed Limit', className='detail_title'), width = 5),
                    dbc.Col([html.P('-', id='rwd_speed',  className='detail_info')], width = 7),
                ]),
                dbc.Row([
                    dbc.Col(html.P('Open Lanes', className='detail_title'), width = 5),
                    dbc.Col([html.P('-', id='rwd_lanes',  className='detail_info')], width = 7),
                ])
            ])
rwd_description = html.Div([
                dbc.Row([
                    dbc.Col(html.P('Phase', className='detail_title'), width = 5),
                    dbc.Col([html.P('-', id='rwd_phase',  className='detail_info')], width = 7),
                ]),
                dbc.Row([
                    dbc.Col(html.P('Description', className='detail_title'), width = 5),
                    dbc.Col([html.P('-', id='rwd_desc',  className='detail_info')], width = 7),
                ])
            ])

# details layout
rw_details = dbc.Card([
                 dbc.CardHeader('Roadwork Details', className='card_header'),
                 html.Div([
                     rwd_header, html.Hr(), rwd_schedule, html.Hr(), rwd_location, html.Hr(), rwd_obstractions, html.Hr(), rwd_description
                 ], className='p-2 alert_box'),
             ], className='card', style={'height': '400px'})

##################
# Roadwork Table
##################
table_col = {'id': 'Index', 'address': 'Address', 'measure': 'Measure', 'start': 'Starting Date', 'end': 'Exp. End Date'}
df_rw = pd.DataFrame([item['metadata'] for item in pp_roadworks])[list(table_col.keys())]

# add state column (if start is in the future -> proposed, end in the past -> completed, rest -> work in progress)
# if estimated end key exists then take this as official scheduled end date
def calc_state(row):
    selected_pp = [p for p in pp_roadworks if p['metadata']['id'] == row['id']][0]
    now = datetime.now()
    start = datetime.strptime(row['start'], '%d.%m.%Y')
    end_date = 'end' if 'estimated' not in selected_pp else 'estimated'
    try:
        end = datetime.strptime(row[end_date], '%d.%m.%Y')
    except ValueError:
        end = datetime.strptime(row[end_date], '%m.%Y')
    if now < start:
        val = 'scheduled'
    elif end < now:
        val = 'completed'
    elif start < now < end:
        val = 'in progress'
    return val
df_rw['state'] = df_rw.apply(calc_state, axis=1)
table_col['state'] = 'State'

# change display of end date
try:
    df_rw['end'] = pd.to_datetime(df_rw['end'], format='%m.%Y').dt.strftime('%B %Y')
except:
    pass

# renaming columns
df_rw = df_rw.rename(columns=table_col)

# font-family to be used
dbc_ff = '-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",Arial,"Noto Sans",sans-serif,"Apple Color Emoji","Segoe UI Emoji","Segoe UI Symbol","Noto Color Emoji"'


rw_table = dbc.Card([
                dbc.CardHeader('Roadwork Table', className='card_header'),
                dtb.DataTable(
                    id = 'rw_table',
                    data = df_rw.to_dict('records'),
                    columns = [{'name': col, 'id': col, 'hidden': True} if col == table_col['id'] else {'name': col, 'id': col} for col in df_rw.columns],
#                    fixed_rows={ 'headers': True, 'data': 0 },
#                    style_table = {'minHeight': '50px', 'overflowY': 'auto', 'height': '350px'},
                    style_header = { 'backgroundColor': '#323232', 'font-family': dbc_ff, 'font-size': '16px', 'font-weight': 'bold', 'color' : 'gold' },
                    style_cell = {
                        'backgroundColor': '#323232', 'color': 'white', 'height': '44px', 'padding': '8px',
                        'border-bottom': '1px solid #7b7b7b', 'border-top': '1px solid #7b7b7b',
                        'font-family': dbc_ff, 'font-size': '16px',
                        'cursor': 'pointer', 'overflow': 'ellipsis', 'text-align': 'left'
                    },
                    style_data_conditional = [{
                        'if': {'column_id': table_col['state'], 'filter_query': f'{{{table_col["state"]}}} eq "scheduled"'}, 'color': '#e7b416'
                    }, {
                        'if': {'column_id': table_col['state'], 'filter_query': f'{{{table_col["state"]}}} eq "completed"'}, 'color': '#99c140'
                    }, {
                        'if': {'column_id': table_col['state'], 'filter_query': f'{{{table_col["state"]}}} eq "in progress"'}, 'color': '#cc3232'
                    }],
                    style_as_list_view = True,
                    # dash-table v4.0.0 has autosize to parent bug, this code takes care of it
                    # last selector disables selection colors (are now the same as defined in style_cell above)
                    css = [{"selector": "div.row.row-1", "rule": "width: 100%;"
                        }, {"selector": "div.cell.cell-1-1", "rule": "width: 100%;"
                        }, {"selector": "table", "rule": "width: 100%;"
                        }, {"selector": '.dash-spreadsheet-container table', "rule": '--accent:#ffffff !important; --selected-background:#676a6f !important;'
                    }]
                )], className = 'card', style = dict(height = '100%'))

##################
# Main Layout
##################
layout = html.Div([
        dbc.Row(dbc.Col(func_tree)),
        dbc.Row([dbc.Col(html.Div(id='rwc', style={'color': 'white'}))]),
        dbc.Row([
            dbc.Col(bing_map, width = 8),
            dbc.Col(rw_details, width = 4),
        ], className = 'py-1'),

        html.Div(rw_table, className = 'py-1'),
        html.Div(id = 'test',  className = 'text-white'),
        html.Div(id = 'roadworks_intermediate',  className = 'd-none')
        ])
