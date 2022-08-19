import time
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import bing_maps_smartcity as bms
from data.bingmaps_data import pp_webcams, pp_energy, pp_congestions
from app import app
from dash.dependencies import Input, Output
#import urllib.request
#import os
#from utils.opencv_helpers import  process_img

##################
# map and cam laoder
##################

imgUrlMarkt = f"https://www.schwaebisch-gmuend.de/files/upload/webcam/marktplatz1/gmuendcam.jpg?rnd={time.time()}"
imgUrlOst = f"https://www.schwaebisch-gmuend.de/webcam_ropa.php?image=weleda.jpg&rnd={time.time()}"

bing_map = dbc.Card([   dbc.CardHeader('Bing Map', className = 'card_header'),
                        bms.BingMaps(id = 'testmap', pushpins = pp_webcams + pp_energy + pp_congestions),
                    ], className = 'card', style={'height': '400px'})

live_img1 = dbc.Card([  dbc.CardHeader('Webcam - Marktplatz', className = 'card_header'),
                        html.Img(
                                id = 'live-img-01',
                                src = imgUrlMarkt,
                                alt = 'Webcam Marktplatz',
                                style = dict(height = '300px', ))
                    ], className = 'card')

live_img2 = dbc.Card([  dbc.CardHeader('Webcam - Tunnel Osteingang', className = 'card_header'),
                         html.Img(
                                 id = 'live-img-02',
                                 src = imgUrlOst,
                                 alt = 'Webcam Marktplatz',
                                 style = dict(height = '300px'))
                    ], className = 'card')

layout = html.Div([
        dbc.Row([
            dbc.Col(bing_map, width = 12),
            ]),

        dbc.Row([
            dbc.Col(live_img1, width = 6),
            dbc.Col(live_img2, width = 6)
            ], className = 'py-2'),

        dcc.Interval(id='map_interval', interval= 10*1000),
        ])

# update
@app.callback([Output('live-img-01', 'src'), Output('live-img-02', 'src')],
              [Input('map_interval', 'n_intervals'),
               ])
def change_image_1 (n):   
    
    #    # for tunnel
    img2 = f"https://www.schwaebisch-gmuend.de/webcam_ropa.php?image=weleda.jpg&rnd={time.time()}"
#    urllib.request.urlretrieve(img1, f'./static/webcam_tun{time_cache}.jpg')
#    process_img(f'./static/webcam_tun{time_cache}.jpg', f'./static/webcam_tun_out{time_cache}.jpg')
#    
#    return f'./static/webcam_tun_out{time_cache}.jpg', f'./static/webcam_mrkt_out{time_cache}.jpg'
    
    # delete old image
#    for fname in os.listdir('./static/'):
#        if fname.startswith("webcam"):
#            os.remove(f'./static/{fname}')
#    time_cache = str(time.time())[-6:]
#
#    #  for market
    img1 = f"https://www.schwaebisch-gmuend.de/files/upload/webcam/marktplatz1/gmuendcam.jpg?rnd={time.time()}"    
#    urllib.request.urlretrieve(img2, f'./static/webcam_mrkt{time_cache}.jpg')
#    process_img(f'./static/webcam_mrkt{time_cache}.jpg', f'./static/webcam_mrkt_out{time_cache}.jpg')
    
    return img1, img2
