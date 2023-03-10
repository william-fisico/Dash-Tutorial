from dash import Dash, html, dcc
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
from PIL import Image
import pydicom

app_teste = Dash(__name__)

img_path = './Y1_pfDicom.dcm'
ds = pydicom.filereader.read_file(img_path)
image_array = ds.pixel_array

sad = ds[0x3002, 0x0022].value
sid = ds[0x3002,0x0026].value
x_res = (ds[0x3002,0x0011].value[0])*(sad/sid)
y_res = (ds[0x3002,0x0011].value[1])*(sad/sid)

dx = 0
dy = 0

x_axis = [(x*x_res/10)-dx for x in range(np.shape(image_array)[0])]
y_axis = [(y*y_res/10)-dy for y in range(np.shape(image_array)[1])]



fig = px.imshow(image_array, x=x_axis, y=y_axis, origin='lower')
fig.update_layout(coloraxis_showscale=False)

# Add traces, one for each slider step
for step in np.arange(0, 24, 1):
    #vis = True if step == 1 else False
    cor = "black" if step == 1 else "red"
    x_line_value = [step for i in x_axis]
    fig.add_trace(go.Scatter(
                            visible=False,
                            line=dict(color=cor, width=1, dash="dash"),
                            x=x_line_value,
                            y=x_axis))
    #fig.add_vline(x=(step-12), line_width=1, line_dash="dash", line_color="green", visible=False)
    ##fig.add_hline(y=0, line_width=1, line_dash="dash", line_color="green", visible=False)

#Horizontal and Vertical Lines and Rectangles in Python
#https://plotly.com/python/horizontal-vertical-shapes/
#fig.add_vline(x=0, line_width=1, line_dash="dash", line_color="green")
#fig.add_hline(y=0, line_width=1, line_dash="dash", line_color="green")

fig.data[10].visible = True

# Create and add slider
steps = []
for i in range(1,len(fig.data)):
    step = dict(
        method="update",
        args=[{"visible": [False] * len(fig.data)},
              {"title": "Slider switched to step: " + str(i)}],  # layout attribute
    )
    step["args"][0]["visible"][i] = True  # Toggle i'th trace to "visible"
    steps.append(step)

sliders = [dict(
    active=10,
    currentvalue={"prefix": "Frequency: "},
    pad={"t": 50},
    steps=steps
)]

fig.update_layout(
    sliders=sliders
)

app_teste.layout = html.Div(children=[
                        html.H1(children='Hello Dash'),
                        html.Div(children='''Dash: A web application framework for your data'''),
                        dcc.Graph(
                                    id='example-graph',
                                    figure=fig
                                )
                    ])

if __name__ == '__main__':
    app_teste.run_server(debug=True)

