from dash import Dash, html, dcc
import plotly.express as px
import numpy as np
from PIL import Image

app_teste = Dash(__name__)

img_path = './Y1.tif'
tiff_file = Image.open(img_path)
image_array = np.array(tiff_file)


fig = px.imshow(image_array)
fig.update_layout(coloraxis_showscale=False)

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