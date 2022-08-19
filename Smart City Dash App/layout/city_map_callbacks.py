# Layout for forecasting page
from dash.dependencies import Input, Output, State
from app import app
import time
from data.bingmaps_data import pp_roadworks, pp_congestions, pp_webcams, pp_energy

# generate pop out info of selected location
@app.callback(Output('map_pop_out', 'is_open'),
              [Input('city-map', 'selected')],
              [State('map_pop_out', 'is_open')])
def pop_up_window (selectedData, is_open):
    if selectedData == None:
        return False
    else:
        return True

# change image
@app.callback([Output('pop_title', 'children'), 
               Output('pop_longitude', 'children'),
               Output('pop_latitude', 'children'), 
               Output('pop_desc', 'children'), 
               Output('cm_pop_image', 'src')
               ],
              [Input('city-map', 'selected'), 
               Input('overview_interval', 'n_intervals'),
               ])
def change_image (selectedData, n):        
    pp_list = pp_roadworks + pp_congestions + pp_webcams + pp_energy
    
    if selectedData != None :
        # the pushpin that match selected data id
        selected_pp = [p for p in pp_list if p['metadata']['id'] == selectedData][0]
        
        # image
        if selected_pp['options']['icon'] == 'roadworksSign':
            img = './static/roadblock-img.jpg'
            
        elif (selected_pp['options']['icon'] in ['solarPark','pvStation']):
            img = './static/solarpark-img.jpg'
            
        elif (selected_pp['metadata']['id'] == 'webcam_01'):
            img = f"https://www.schwaebisch-gmuend.de/files/upload/webcam/marktplatz1/gmuendcam.jpg?rnd={time.time()}"
            
        else:
            img = f"https://www.schwaebisch-gmuend.de/webcam_ropa.php?image=weleda.jpg&rnd={time.time()}"
        
        # description
        if selected_pp['options']['icon'] == 'roadworksSign':
            title = selected_pp['metadata']['address']
            desc = 'Scheduled End Time: ' + selected_pp['metadata']['end']
        else:
            title = selected_pp['metadata']['title']
            desc = selected_pp['metadata']['description']
        
        return title, selected_pp['location'][0], selected_pp['location'][1],  desc, img
    else:
        return [],[],[],[],[]
    
@app.callback(
    Output("overview_tree_collapse", "is_open"),
    [Input("overview_tree_button", "n_clicks")],
    [State("overview_tree_collapse", "is_open")],
)
def toggle_tree_collapse(n, is_open):
    if n:
        return not is_open
    return is_open