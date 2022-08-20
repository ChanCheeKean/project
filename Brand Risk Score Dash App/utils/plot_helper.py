'''Plotly Helper'''
import pandas as pd
import numpy as np
import plotly.graph_objs as go
import plotly.figure_factory as ff

bg_color = 'rgba(0,0,0,0)'
paper_color = 'rgba(0,0,0,0)'
txt_color = 'white'
color_list = ['#FCB71A', '#FF5050', '#1082C5', '#33CCCC', 'rgb(241, 89, 39)', 'rgb(51, 204, 204)', 'rgb (123, 102, 255)', 'rgb(16, 130, 197)', 'rgb(0, 204, 255)',]
color_list_2 = ['rgb(51, 204, 204)', 'rgb(241, 89, 39)', 'rgb (123, 102, 255)', 'rgb(16, 130, 197)', 'rgb(0, 204, 255)',]
font_size = 10
font_family = 'Verlag'
font=dict(size=font_size, family='Verlag')

def get_joint_plot(df_x, df_y, xtitle=None, ytitle=None, width=None, height=None, title=None):
    data=[
        go.Scatter(
            x=df_x, 
            y=df_y, 
            mode='markers',
            name='points',
            marker=dict(color=color_list[0], size=3)), 
                
        go.Histogram(
            x=df_x, 
            name=xtitle,
            marker=dict(color=color_list[1]),
            marker_line_width=1,
            histnorm='probability',
            nbinsx=50, 
            yaxis='y2'),
        
        go.Histogram(
            y=df_y, 
            name=ytitle, 
            marker=dict(color=color_list[2]),
            marker_line_width=1,
            histnorm='probability',
            nbinsx=50, 
            xaxis='x2')]
    
    layout=go.Layout(
        font=dict(size=font_size, color=txt_color, family=font_family), 
        width=width, 
        height=height,
        title=title,
        title_x=0.5,
        titlefont=dict(size=12, color=txt_color), 
        hovermode='closest',
        bargap=0,
        showlegend=False,
        autosize=False,
        xaxis=dict(title=xtitle, titlefont=dict(color=txt_color), domain=[0, 0.85], showgrid=False, zeroline=False),
        yaxis=dict(title=ytitle, titlefont=dict(color=txt_color), domain=[0, 0.75], showgrid=False, zeroline=False),
        xaxis2=dict(title='Density', domain=[0.85, 1], showgrid=False, zeroline=True),
        yaxis2=dict(title='Density', domain=[0.75, 1], showgrid=False, zeroline=True),
        plot_bgcolor=bg_color, 
        paper_bgcolor=paper_color,
        margin=dict(l=70, r=10, t=10, b=20))
    return go.Figure(data=data, layout=layout)

def get_dist_plot(df, xtitle=None, ytitle=None, title=None, width=None, height=None, bins=30, **kwargs):
    fig = ff.create_distplot([df[col] for col in df.columns], df.columns, colors=color_list, bin_size=bins, **kwargs)
    fig.update_layout(
        font=dict(size=font_size, color=txt_color, family=font_family), 
        width=width, 
        height=height,
        title=title,
        title_x=0.5,
        titlefont=dict(size=12, color=txt_color), 
        showlegend=True,
        legend_orientation="h",
        legend=dict(x=.6, y=-0.1, font=dict(size=10)),
        xaxis=dict(title=xtitle, titlefont=dict(color=txt_color), showgrid=False,),
        yaxis=dict(title=ytitle, titlefont=dict(color=txt_color), tickformat='.2f', ticks="outside", ticklen=5), 
        plot_bgcolor=bg_color, 
        paper_bgcolor=paper_color,
        margin=dict(l=10, r=10, t=10, b=10))
    return fig

def get_histrogram(df_x, xtitle=None, ytitle=None, title=None, width=300, height=250, bins=None):
    traces = [
        go.Histogram(
            x=df_x,
            nbinsx=bins, 
            marker_line_width=1,
            marker_color=color_list,
            marker_line_color=color_list)]
    layout = go.Layout(
        font=dict(size=font_size, color=txt_color, family=font_family), 
        width=width, 
        height=height,
        title=title,
        title_x=0.5,
        titlefont=dict(size=12, color=txt_color), 
        xaxis=dict(title=xtitle, titlefont=dict(color=txt_color)),
        yaxis=dict(title=ytitle, titlefont=dict(color=txt_color), tickformat='.2f'), 
        plot_bgcolor=bg_color, 
        paper_bgcolor=paper_color,
        margin=dict(l=100, r=10, t=40, b=10))
    return go.Figure (data=traces, layout=layout)

def get_pie_chart(df, width=None, height=None, title=None):
    data=[
        go.Pie(
        labels=df.index, 
        values=df.values,
        # marker=dict(colors=color_list),
        )]
    layout = go.Layout(
        font=dict(size=font_size, color=txt_color, family=font_family), 
        width=width, 
        height=height,
        title=title,
        title_x=0.5,
        titlefont=dict(size=12, color=txt_color), 
        plot_bgcolor=bg_color, 
        paper_bgcolor=paper_color,
        margin=dict(l=10, r=10, t=10, b=10))
    return go.Figure (data=data, layout=layout)

def get_histrogram_x(df_x, cat, values, mode='overlay', width=None, height=None, xtitle=None, ytitle=None, title=None, bins=None, norm=""):
    traces = [
        go.Histogram(
            x=df_x[df_x[cat] == name][values],
            nbinsx=bins, 
            name=str(name),
            marker_color=color_list[count],
            opacity=0.9,
            histnorm=norm,
            marker_line_width=1) for count, name in enumerate(df_x[cat].unique())]
        
    layout = go.Layout(
        font=dict(size=font_size, color=txt_color, family=font_family), 
        width=width, 
        height=height,
        barmode=mode,
        title=title,
        title_x=0.5,
        titlefont=dict(size=12, color=txt_color), 
        legend_orientation="h",
        legend=dict(x=0.4, y=1.1, font=dict(size=10)),
        xaxis=dict(title=xtitle, titlefont=dict(color=txt_color)),
        yaxis=dict(title=ytitle, titlefont=dict(color=txt_color), tickformat='.2f', gridcolor='white'), 
        plot_bgcolor=bg_color, 
        paper_bgcolor=paper_color,
        margin=dict(l=70, r=10, t=10, b=10))
    fig = go.Figure (data=traces, layout=layout)    
    return fig

def get_bar_h(df, xtitle=None, ytitle=None, title=None, width=None, height=300):    
    traces=[
        go.Bar(
            x=row[1].values.tolist(),
            y=df.columns,
            orientation='h',
            marker_line_width=1,
            marker_color=color_list_2[count],
            marker_line_color='white',
            name=row[0],
            opacity=0.8) for count, row in enumerate(df.iterrows())]
    
    layout = go.Layout(
        font=dict(size=font_size, color=txt_color, family=font_family), 
        width=width, 
        height=height,
        title=title,
        title_x=0.5,
        titlefont=dict(size=12, color=txt_color), 
        showlegend=True,
        legend_orientation="h",
        bargap=0.30,
        legend=dict(x=.6, y=-.15, font=dict(size=10)),
        xaxis=dict(title=xtitle, titlefont=dict(color=txt_color)),
        yaxis=dict(title=ytitle, titlefont=dict(color=txt_color), tickformat='.2f', ticks="outside", ticklen=5), 
        plot_bgcolor=bg_color, 
        paper_bgcolor=paper_color,
        margin=dict(l=70, r=0, t=10, b=10))
    return go.Figure (data=traces, layout=layout)

def get_ts_plot(df_x, title=None, yaxis_label=None, xaxis_label=None, width=None, height=None, hover_mode='x', legend_bool=True, xtick=0, drag_mode='zoom'):
    try:
        traces = [go.Scattergl(
            x=df_x.index, 
            y=df_x[name].round(2),
            mode='markers + lines',
            name=name, 
            marker=dict(size=6), 
            marker_color=color_list[count],
            line=dict(width=2)) for count, name in enumerate(df_x.columns)]
    except:
        traces = [go.Scattergl(
            x=df_x.index, 
            y=df_x.round(2), 
            mode='markers + lines', 
            name=df_x.name,
            marker=dict(size=6, color='blue'), 
            line=dict(width=2, color='blue'))]
    layout = go.Layout(
        font=dict(size=font_size, color=txt_color, family=font_family), 
        width=width, 
        height=height,
        title=title,
        title_x=0.5,
        titlefont=dict(size=12, color=txt_color), 
        showlegend=legend_bool,
        legend_orientation="h",
        legend=dict(x=0, y=1.1, font=dict(size=10)),
        xaxis=dict(dtick=xtick, title=xaxis_label, titlefont=dict(color=txt_color), gridcolor='rgba(0,0,0,0)'),
        yaxis=dict(title=yaxis_label, titlefont=dict(color=txt_color), tickformat='.2f', ticklen=5, gridcolor='white', gridwidth=1), 
        plot_bgcolor=bg_color, 
        paper_bgcolor=paper_color,
        hovermode=hover_mode,
        dragmode=drag_mode, 
         margin=dict(l=50, r=20, t=5, b=30))
    fig=go.Figure (data=traces, layout=layout)
    return fig

def get_radar_plot(df, radial_range=[0, 10], width=None, height=None):
    data = [go.Scatterpolar(
        r=list(row[1].values) + [row[1].values[0]], 
        theta=list(df.columns) + [df.columns[0]], 
        marker_line_width=2,
        marker_color=color_list[count + 1],
        fill='toself',
        name=row[0],
        opacity=0.9) for count, row in enumerate(df.iterrows())]
    
    layout = go.Layout (
        width=width,
        height=height,
        font=dict(size=font_size, color=txt_color, family=font_family), 
        polar=dict(bgcolor='rgba(0, 0, 0, 0)', radialaxis=dict(visible=True, range=radial_range), angularaxis_categoryarray=df.columns), 
        # legend_orientation='h',
        showlegend=True, 
        legend=dict(x=0, y=1, font=dict(size=12, color=txt_color)),
        plot_bgcolor=bg_color, 
        paper_bgcolor=paper_color,
        margin=dict(l=5, r=5, t=20, b=20))
    fig=go.Figure (data=data, layout=layout)
    return fig

def get_mapbox(lat=[0], lon=[0], size=[10], color=None, text=None, showlegend=False, showscale=True, 
               hovermode='x', dragmode='pan', clickmode='event+select', center_lat=0, center_lon=0, zoom=2, height=None, width=None):            
        mapbox_access_token="pk.eyJ1IjoiY2hhbmNoZWVrZWFuIiwiYSI6ImNqdjgzYmYzNjBmeDQzem43MzIwcnI1djMifQ.igdgIdtTUOVIAXO7WA2ZBw" 
        data=[go.Scattermapbox(
            lat=lat, 
            lon=lon, 
            text=text, 
            hoverinfo='text',
            mode='markers',
            marker=dict(size=size, color=color, colorscale= 'YlOrRd', showscale=showscale, reversescale=True))]
        layout=go.Layout(
                width=width,
                height=height,
                font=dict(size=font_size, color=txt_color, family=font_family), 
                autosize=True, 
                showlegend=showlegend,
                hovermode=hovermode, 
                dragmode=dragmode, 
                clickmode=clickmode,
                plot_bgcolor=bg_color, 
                paper_bgcolor=paper_color,
                margin=dict(l=0, r=0, t=0, b=0),
                mapbox=dict(accesstoken=mapbox_access_token, bearing=0, style='dark', center=dict(lat=center_lat, lon=center_lon), pitch=0, zoom=zoom))
        fig=go.Figure(data=data, layout=layout)
        return fig

def get_ts_s1(df, target, width=None, height=None, lw=0):
    # set upper and lower limit
    
    lsl = lw
    # mean = df[target].median()
    d1 = df[df[target] <= lsl].rename(columns={target: "outlier"})
    # plotting
    
    data = [
        go.Scattergl(
            x=df.index, 
            y=df[target],
            mode='markers+lines', 
            marker=dict(size=5, color=color_list[3]),
            line=dict(width=2.5, color=color_list[3]),
            name='Trust Score'),  
        
        # go.Scattergl(
        #     x=df.index, 
        #     y=df['Rolling_Mean'],
        #     mode='markers+lines', 
        #     marker=dict(size=5, color='gold'),
        #     line=dict(width=2.5, color='gold', dash='dash',),
        #     name='7 - Rolling Mean'), 
        
        go.Scattergl(
            x=d1.index, 
            y=d1['outlier'],
            mode='markers', 
            marker=dict(size=15, color=color_list[1], symbol='diamond-open-dot', line=dict(width=2)),
            name='Out of Control')]
    
    layout = go.Layout(
        width=width,
        height=height,
        font=dict(size=font_size, color=txt_color, family=font_family), 
        legend_orientation="h",
        legend=dict(x=0, y=1.2),
        hovermode='closest',
        dragmode='zoom', 
        showlegend=True,
        xaxis=dict(gridcolor='rgba(0,0,0,0)'),
        yaxis=dict(tickformat='.2f', ticklen=5, gridcolor='white', gridwidth=1,), 
        plot_bgcolor=bg_color, 
        paper_bgcolor=paper_color,
        margin = dict(l=10, r = 10, t=10, b = 10))
    
    fig = go.Figure(data=data, layout=layout)
    
    # straight line and annotations
    fig['layout'].update(
        shapes = [
            # Upper Limit
            # go.layout.Shape(type='line', xref="x", yref="y", x0=df.index.min(), y0=usl, x1=df.index.max(), y1=usl, line={"color": "rgb(255,127,80)", "width": 2, "dash": "dot"},),
            # Lower Limit           
            go.layout.Shape(type='line', xref="x", yref="y", x0=df.index[0], y0=lsl, x1=df.index[-1], y1=lsl, line={"color": "rgb(255,127,80)", "width": 2, "dash": "dot"},),
            # mean
            # go.layout.Shape(type='line', xref="x", yref="y", x0=df.index[0], y0=mean, x1=df.index[-1], y1=mean, line={"color": color_list[0], "width": 3, "dash": "dot"},)
            ],
        
        annotations=[
            go.layout.Annotation(x=0.5, y=lsl -3, xref="paper", yref="y", text="Lower Limit:  " + str(round(lsl, 2)), showarrow=False, font={"color": 'gold', "size" : 12},),
            # go.layout.Annotation(x=0.5, y=usl + 3, xref="paper", yref="y", text="Upper Limit:" + str(round(usl, 2)), showarrow=False, font={"color": 'gold', "size" : 12},),
            # go.layout.Annotation(x=0.5, y=mean + 4, xref="paper", yref="y", text="Mean:  " + str(round(mean, 2)), showarrow=False, font={"color": 'gold', "size" : 12},)
            ])
    return fig
    
################
### Reserved ###
################

def get_corr_heatmap(df, title=None, height=300, width=900, grouped=False, zmax=1, zmin=0):    
    df = df.corr()
    if grouped:
        df.index = [x[0] + ': ' + x[1] for x in df.index]
    fig = ff.create_annotated_heatmap(
        z=df.values.round(2), 
        x=df.columns.tolist(), 
        y=df.index.tolist(), 
        reversescale=True,
        zmin=zmin,
        zmax=zmax,
        showscale=True)
    fig['layout']['yaxis']['autorange']="reversed"
    fig['layout'].update(
        width=width, 
        height=height,
        font=dict(size=font_size, color=txt_color, family=font_family), 
        title=title, 
        title_x=0.5,
        titlefont=dict(size=12, color=txt_color), 
        plot_bgcolor=bg_color, 
        paper_bgcolor=paper_color,
        margin=dict(l=10, r=10, t=80, b=10))
    return fig

def get_boxplot_cat(df_y, cat, values, xtitle=None, ytitle=None, width=None, height=None, title='title'):
    traces = [go.Box(
        y=df_y[df_y[cat] == name][values], 
        name=name,
        boxpoints='outliers', 
        jitter=0, 
        marker_color=color_list,
        marker=dict(size =2)) for name in df_y[cat].unique()]
    layout = go.Layout(
        font=dict(size=font_size, color=txt_color, family=font_family), 
        width=width, 
        height=height,
        title=title,
        title_x=0.5,
        titlefont=dict(size=12, color=txt_color), 
        showlegend=True,
        legend_orientation="h",
        legend=dict(x=1, y=-0.95, font=dict(size=10)),
        xaxis=dict(title=xtitle, titlefont=dict(color=txt_color), ticklen=5),
        yaxis=dict(title=ytitle, titlefont=dict(color=txt_color), tickformat='.2f'), 
        plot_bgcolor=bg_color, 
        paper_bgcolor=paper_color,
        margin=dict(l=50, r=10, t=40, b=0))
    return go.Figure (data=traces, layout=layout)