from dash.dependencies import Input, Output, State
from datetime import datetime
from app import app
from data.bingmaps_data import pp_roadworks

table_id = []
pushpin_id = []

# expand/collapse story chart
@app.callback(
    Output("roadworks_tree_collapse", "is_open"),
    [Input("roadworks_tree_button", "n_clicks")],
    [State("roadworks_tree_collapse", "is_open")],
)
def toggle_congestion_collapse(n, is_open):
    if n:
        return not is_open
    return is_open

# reflect roadwork details according to selected pushpins
@app.callback(
     [Output('rwd_header', 'children'), Output('rwd_id', 'children'),
      Output('rwd_start', 'children'),Output('rwd_end', 'children'),
      Output('rwd_est', 'children'), Output('rwd_loc', 'children'),
      Output('rwd_speed', 'children'), Output('rwd_lanes', 'children'),
      Output('rwd_phase', 'children'), Output('rwd_desc', 'children'),
      ],
     [Input('roadwork_map', 'selected')])
def update_details(selected):

    selected_pp = [p for p in pp_roadworks if p['metadata']['id'] == selected][0]
    pp_data = selected_pp['metadata']
    start_time = datetime.strptime(pp_data['start'], '%d.%m.%Y')
    try:
        end_time = datetime.strptime(pp_data['end'], '%d.%m.%Y')
    except ValueError:
        end_time = datetime.strptime(pp_data['end'], '%m.%Y')
    except:
        pass
    now_time = datetime.now()

    rwd_header = pp_data['measure']
    rwd_id = 'System ID: ' + pp_data['id']
    rwd_start = pp_data['start']
    rwd_end = pp_data['end']
    rwd_est = pp_data['end'] if 'estimated' not in pp_data else pp_data['estimated']
    rwd_loc  = pp_data['address']
    rwd_desc  = pp_data['description']
    # obstructions
    if 'obstruction' in pp_data:
        rwd_speed  = str(pp_data['obstruction']['speed_limit']) + ' kM/h' if 'speed_limit' in pp_data['obstruction'] else 'No speed limit imposed'
        if 'lanes' not in pp_data['obstruction']:
            "All lanes open"
        elif isinstance(pp_data['obstruction']['lanes'], int):
            rwd_lanes = str(pp_data['obstruction']['lanes']) + ' lane(s) open'
        elif isinstance(pp_data['obstruction']['lanes'], str):
            rwd_lanes = pp_data['obstruction']['lanes']
    else:
        rwd_speed = 'No carriageway incursion'
        rwd_lanes = 'All lanes open'
    # phase
    if 'phase' not in pp_data:
        if start_time > now_time:
            rwd_phase = "Planning"
        elif start_time < now_time < end_time:
            rwd_phase = "In progress"
        elif now_time > end_time:
            rwd_phase = "Works finished"
    else:
        rwd_phase = pp_data['phase']

    return rwd_header, rwd_id, rwd_start, rwd_end,  rwd_est, rwd_loc, rwd_speed, rwd_lanes, rwd_phase, rwd_desc


# update detail from selected table cell
# it will update the selected pushpin on map, and the map will update detail
@app.callback(
    Output('roadwork_map', 'selected'),
    [Input('rw_table', 'selected_cells')],
    [State('rw_table','data')]
 )
def update_details_from_map(active_cell, data):
    row_num = active_cell[0]['row']
    return str(data[row_num]['Index'])

# highlighting row corresponding to selected pushpin
@app.callback(
    Output('rw_table', 'style_data_conditional'),
    [Input('roadwork_map', 'selected')],
    [State('rw_table', 'style_data_conditional')]
 )
def highlight_row(selected, existing_style):

   if len(existing_style) > 3:
       existing_style = [filter for filter in existing_style if 'column_id' in filter['if'].keys()]
   new_style = existing_style
   if selected != None:
       row_index = [rw['metadata'] for rw in pp_roadworks if rw['metadata']['id']==selected][0]['id']
       style_filter = {
           'if': {'filter_query': f'{{Index}} eq {row_index}'},
           'backgroundColor': '#676a6f',
           'border': '1px solid #ffffff',
       }
       new_style.append(style_filter)
   return new_style


# clear selector css when clicking pushpin
@app.callback(Output('rw_table', 'css'),
               [Input('roadwork_map', 'selected'), Input('rw_table', 'selected_cells')],
               [State('rw_table','data')]
 )
def highlight_selector_css(selectedpushpin, selected_table, data):
   global pushpin_id, table_id
   row_num = selected_table[0]['row']
   table_id = data[row_num]['Index']
   pushpin_id = selectedpushpin

   if pushpin_id == table_id:
       css = [{"selector": "div.row.row-1", "rule": "width: 100%;"
               }, {"selector": "div.cell.cell-1-1", "rule": "width: 100%;"
               }, {"selector": "table", "rule": "width: 100%;"
               }, {"selector": '.dash-spreadsheet-container table', "rule": '--accent:#ffffff !important; --selected-background:#676a6f !important;'
                   }]
   else:
        css = [{"selector": "div.row.row-1", "rule": "width: 100%;"
               }, {"selector": "div.cell.cell-1-1", "rule": "width: 100%;"
               }, {"selector": "table", "rule": "width: 100%;"
               }, {"selector": '.dash-spreadsheet-container table', "rule": '--accent:#7b7b7b !important; --selected-background:#323232 !important;'
                   }]
   return css
