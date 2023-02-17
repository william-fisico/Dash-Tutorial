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




fig = go.Figure()

for step in np.arange(0, 23, 1):
    x_axis = [(x*x_res/10)-12.5 for x in range(np.shape(image_array)[0])]
    y_axis = [(y*y_res/10)-step for y in range(np.shape(image_array)[1])]
    y_line_value = [0 for i in y_axis]
    fig.add_trace(
            go.Heatmap(z=image_array, x=x_axis, y=y_axis, visible=False)
        )
    fig.add_trace(
            go.Scatter(visible=False, line=dict(color="green", width=1, dash="dash"),
                        y=y_line_value, x=x_axis)
        )

fig.update_layout(width=700, height=700, autosize=True)

fig.data[0].visible = True
fig.data[1].visible = True

steps = []
for i in range(0,len(fig.data),2):
    step = dict(
        method="update",
        args=[{"visible": [False] * len(fig.data)},
              {"title": "Slider switched to step: " + str(i)}],  # layout attribute
    )
    step["args"][0]["visible"][i] = True  # Toggle i'th trace to "visible"
    step["args"][0]["visible"][i+1] = True  # Toggle i'th trace to "visible"
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

