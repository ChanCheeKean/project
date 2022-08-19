import plotly.graph_objs as go
import plotly.figure_factory as ff

bg_color = '#323232'
txt_color = 'white'

def get_ts_plot(df_1, title = 'Time Series Plot', yaxis_label = ' ', xaxis_label = 'TimeFrame', hover_mode = 'x', 
                legend_bool = True, convert_x = True, xtick = 0, drag_mode = 'zoom', ):
    
    if convert_x == True:
        x = df_1.index.tz_localize('UTC').tz_convert('US/Eastern')
    else:
        x = df_1.index
    try:
        traces = [
                go.Scattergl(
                        x = x, 
                        y = df_1[name].round(2),
                        mode = 'markers+lines',
                        name = name, 
                        marker = dict(size =2), 
                        line = dict(width = 1)) 
                for name in df_1.columns
                ]
    except:
        traces = [
                go.Scattergl(
                         x = x, 
                         y = df_1.round(2), 
                         mode = 'markers+lines', 
                         name = df_1.name,
                         marker = dict(size=2, color='blue'), 
                         line = dict(width=1, color='blue')
                        )]
                
    layout = go.Layout (
            title=title, 
            font=dict(size = 10),
            titlefont =dict(size = 14, color = '#0e4886'), 
            hovermode = hover_mode,
            dragmode = drag_mode, 
            xaxis = dict(dtick = xtick, title = xaxis_label, titlefont = dict(color = '#0e4886')),
            showlegend = legend_bool,
            yaxis = dict(title = yaxis_label, titlefont = dict(color = '#0e4886'), tickformat = '.2f'), 
            margin = dict(l = 90, r = 10, t = 25, b = 40))
        
    fig = go.Figure (data = traces, layout = layout)
    return fig

def get_ts_plot_2(df_1, df_2, title = 'Anomaly Detection', yaxis_label = ' ', xaxis_label = 'TimeFrame', hover_mode = 'closest'):
        
    d1 = go.Scattergl(
            x = df_1.index,
            y = df_1.round(2), 
            text = df_1.index,
            mode = 'markers+lines', 
            name = df_1.name, 
            marker = dict(size =2, color = 'blue'), 
            line = dict(width = 1, color = 'blue')) 
    
    d2 = go.Scattergl(
            x = df_2.index,
            y = df_2.round(2), 
            text = df_2.index,
            mode = 'markers+lines',
            name = df_2.name,
            marker = dict(size =2, color = 'orange'), 
            line = dict(width = 1, color = 'orange')) 
        
    layout = go.Layout (
            title = title, 
            font = dict(size = 10),
            titlefont = dict(size = 14, color = '#0e4886'), 
            hovermode = hover_mode,
            xaxis = dict(title = xaxis_label, titlefont = dict(color = '#0e4886')),
            showlegend = True,
            yaxis = dict(title = yaxis_label, titlefont = dict(color = '#0e4886'), tickformat = '.2f'), 
            margin = dict(l = 90, r = 10, t = 25, b = 40))
        
    fig = go.Figure (data = [d1,d2], layout = layout)
    return fig

def get_ts_plot_outlier(df_1, df_2, title = 'Anomaly Detection', yaxis_label = ' MAD', xaxis_label = 'TimeFrame', hover_mode = 'closest'):   
    d1 = go.Scattergl(
            x = df_1.index.tz_localize('UTC').tz_convert('US/Eastern'), 
            y = df_1.round(2), 
            text = df_1.index,
            mode = 'markers+lines', 
            name = yaxis_label, 
            marker = dict(size =2, color = 'blue'), 
            line = dict(width = 1, color = 'blue')) 
    
    d2 = go.Scattergl(
            x = df_2.index.tz_localize('UTC').tz_convert('US/Eastern'), 
            y = df_2.round(2), 
            text = df_2.index,
            mode = 'markers',
            name = 'Anomaly',
            marker = dict(size =10, color = 'red'))
        
    layout = go.Layout (title = title, 
                        titlefont = dict(size = 16), 
                        hovermode = hover_mode,
                        xaxis = dict(title = xaxis_label, titlefont = dict(color = '#0e4886')),
                        yaxis = dict(title = yaxis_label, titlefont = dict(color = '#0e4886')),
                        font = dict(size = 10), 
                        margin = dict(l = 45, r = 10, t = 35, b = 40))
    
    fig = go.Figure (data = [d1,d2], layout = layout)
    return fig

def get_box_plot(df_trans, title = 'Box Plot', y_label = 'Temperature [°C]', legend_bool = True):
                        
    traces = [
            go.Box(
                    y = df_trans[name], 
                    text = df_trans[name].index, 
                    name = name,
                    boxpoints = 'outliers', 
                    jitter = 0, 
                    marker = dict(size =2),
                    ) 
            for name in df_trans.columns
            ]     
    
    layout = go.Layout (
            title =  title, 
            titlefont = dict(size = 14, color = '#0e4886'),
            legend = dict(x = 1, y = 0.95, font = dict(size = 10)),
            showlegend = legend_bool,
            yaxis = dict(title = y_label, titlefont = dict(color = '#0e4886'), tickformat  = '.1f'),
            font = dict(size = 10), margin = dict(l = 60, r = 5, t = 30, b = 30)
            )
    fig = go.Figure (data = traces, layout = layout)
    return fig

def get_mapbox(df_map, lat, lon, text, cat, symbol_dict, center_lat = 0, center_lon = 0, zoom = 2):            
        mapbox_access_token = "pk.eyJ1IjoiY2hhbmNoZWVrZWFuIiwiYSI6ImNqdjgzYmYzNjBmeDQzem43MzIwcnI1djMifQ.igdgIdtTUOVIAXO7WA2ZBw" 
        data = []
        size_list = [25,20,10]
        color_list = ['red','white','white']
        
        for cat_count in df_map[cat].unique():
            s = symbol_dict[cat_count]
            df = df_map[df_map.cat == cat_count]
            for i in range (0,3):
                size = size_list [i]
                color = color_list [i]
                s = symbol_dict[cat_count] if i == 2 else 'circle'

                data.append(
                    go.Scattermapbox(
                        lat = df[lat], 
                        lon = df[lon], 
                        text = df[text], 
                        hoverinfo = 'text',
                        name = cat_count,
                        marker = dict(
                                size = size, 
                                color = color,
                                symbol = s)))
        
        layout = go.Layout(
                autosize=True, 
                hovermode='closest', 
                dragmode = 'select', 
                clickmode = 'event+select',
#                plot_bgcolor = '#F0F0F0', paper_bgcolor = '#F0F0F0',
                showlegend = False,
                font = dict(size = 10),
                margin = dict(l = 0, r = 0, t = 0, b = 0),
                mapbox=dict(accesstoken=mapbox_access_token, bearing = 0, style="outdoors",
                center=dict(lat = center_lat, lon = center_lon), pitch=0, zoom = zoom)
                )
        fig = go.Figure(data=data, layout=layout)
        return fig

def get_heatmap(df_1, x_value, y_value, measurement_names, title = '', x_title = '', y_title = ''):
    
    dh = df_1.pivot_table(columns= x_value, index= y_value, values = measurement_names)        
    data = [go.Heatmap(y= dh.index, x = dh.columns, z = dh.values, colorscale= 'Viridis')]
    layout = go.Layout(
                        title = title, 
                        margin = dict(l = 40, r = 0, t = 25, b = 40), 
                        titlefont = dict(size = 15, color = '#0e4886'), 
                        xaxis = dict(dtick = 1,tickfont = dict(size=9), 
                        title = x_title, 
                        titlefont = dict(color = '#0e4886')), 
                        yaxis = dict(dtick = 1, tickfont = dict(size=9), 
                        title = y_title, 
                        titlefont = dict(color = '#0e4886')), 
                        font = dict(size = 10))
    fig = go.Figure (data = data, layout = layout)
    return fig

def get_corr_heatmap(df_1, title = 'Linear Correlation Heatmap'):
    df_2 = df_1.corr()
    fig = ff.create_annotated_heatmap(
            z = df_2.values.round(2), 
            x=df_2.columns.tolist(), 
            y=df_2.index.tolist(), 
            colorscale='Viridis', 
            showscale = True,
            )
    fig['layout'].update(
            title = title, 
            titlefont = dict(size = 15, color = '#0e4886'), 
            margin = dict(l = 70, r = 20, t = 30, b = 10), 
            font = dict(size = 10)
            )
    return fig

def get_scatter_plot (df_trans, x, y, title = 'Scatter Plot'):
        trace1 = go.Scattergl( 
                    x = df_trans[x], 
                    y = df_trans[y],  
                    text = df_trans[x].index,
                    mode = 'markers', 
                    marker = dict(size =2)
                    )
        trace2 = go.Box(
                x = df_trans[x], 
                text = df_trans[x].index, 
                name = x, 
                boxpoints = 'outliers', 
                jitter = 0, 
                marker = dict(size =2),
                yaxis = 'y2')
        trace3 = go.Box(
                y = df_trans[y], 
                text = df_trans[y].index, 
                name = y, 
                boxpoints = 'outliers', 
                jitter = 0, 
                marker = dict(size =2),
                xaxis = 'x2')
        vs_traces = [trace1, trace2, trace3]
        vs_layout = go.Layout (
                title = title .format(x,y), hovermode = 'closest',
                titlefont = dict(size = 14, color = '#0e4886'), 
                xaxis = dict(tickfont = dict(size=10), 
                             titlefont = dict(color = '#0e4886'),
                             title = x, 
                             domain = [0, 0.85], 
                             showgrid = False), 
                xaxis2 = dict( domain = [0.85, 1], 
                              showticklabels=False, 
                              showgrid = False),
                yaxis = dict(tickfont = dict(size=10), 
                             title = y, 
                             titlefont = dict(color = '#0e4886'),
                             domain = [0, 0.85], 
                             showgrid = False), 
                yaxis2 = dict(domain = [0.85,1], 
                              showticklabels=False, 
                              showgrid = False),
                showlegend = False,
                font = dict(size = 10), margin = dict(l = 45, r = 5, t = 30, b = 30))
                            
        fig = go.Figure (data = vs_traces, layout = vs_layout)
        return fig
    
def get_bar_chart(d1, d2, y_var, x_var):
    
    data = [
            go.Bar(
            x = d1[y_var], 
            y = d1[x_var], 
            orientation='h',
            name = 'From Town'
            ),
                    
            go.Bar(
            x = d2[y_var], 
            y = d2[x_var], 
            orientation='h',
            name = 'To Town'
            )]
    
    layout = go.Layout (
#            legend_orientation="h",
            showlegend = True,
            plot_bgcolor = bg_color, paper_bgcolor = bg_color,
            yaxis = dict(ticklen=5),
            font = dict(size = 10, color = txt_color), margin = dict(l = 50, r = 5, t = 30, b = 30),
            )
        
    fig = go.Figure (data = data, layout = layout)
    return fig

def get_parking_scatter_plot(df_trans, vtype, vtime, gridline = False):

    df_trans = df_trans[df_trans.Type == vtype]        
    df_trans['text'] = df_trans.index.astype(str) + '<br>' + df_trans['Car_ID'] + '<br>'+ df_trans[vtime].astype(str) + 'mins'
        
    data = go.Scattergl( 
            x = df_trans[vtime], 
            y = df_trans['Type'], 
            text = df_trans['text'],
            mode = 'markers', 
            hoverinfo="text",
            marker = dict(size = 6, color = 'gold'))
        
    layout = go.Layout (
            hovermode = 'closest',
            showlegend = False,
            font = dict(size = 10, color = 'white'),
            plot_bgcolor = bg_color, paper_bgcolor = bg_color,
            xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
            yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
            margin = dict(l = 45, r = 5, t = 5, b = 20))
                            
    fig = go.Figure (data = [data], layout = layout)
    
    if gridline == True:
        fig['layout'].update(xaxis=dict(showticklabels=True),yaxis=dict(zeroline=True))
    return fig
    