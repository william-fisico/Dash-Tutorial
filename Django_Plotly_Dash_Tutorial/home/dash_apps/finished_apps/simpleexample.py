from dash import Dash, html, dcc
from dash.dependencies import Input, Output
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
from PIL import Image
import pydicom
from django_plotly_dash import DjangoDash

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = DjangoDash('SimpleExample', external_stylesheets=external_stylesheets)

img_path = './static/Y1_pfDicom.dcm'
ds = pydicom.filereader.read_file(img_path)
image_array = ds.pixel_array

sad = ds[0x3002, 0x0022].value
sid = ds[0x3002,0x0026].value
x_res = (ds[0x3002,0x0011].value[0])*(sad/sid)
y_res = (ds[0x3002,0x0011].value[1])*(sad/sid)

dx = 12.75
dy = 21.3

x_axis = [(x*x_res/10)-dx for x in range(np.shape(image_array)[0])]
y_axis = [(y*y_res/10)-dy for y in range(np.shape(image_array)[1])]



fig = px.imshow(image_array, x=x_axis, y=y_axis, origin='lower')
fig.update_layout(coloraxis_showscale=False)

#Horizontal and Vertical Lines and Rectangles in Python
#https://plotly.com/python/horizontal-vertical-shapes/
fig.add_vline(x=0, line_width=1, line_dash="dash", line_color="green")
fig.add_hline(y=0, line_width=1, line_dash="dash", line_color="green")


app.layout = html.Div(children=[
                        html.H1(children='Hello Dash'),
                        html.Div(children='''Dash: A web application framework for your data'''),
                        dcc.Graph(
                                    id='example-graph',
                                    figure=fig
                                )
                    ])