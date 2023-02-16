# Import libraries
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import json
import ipywidgets as widgets

x=np.random.uniform(-10,10,size=50)
y=np.sin(x)

fig=go.FigureWidget([go.Scatter(x=x, y=y, mode='markers'), go.Scatter(x=[], y=[], mode="lines")])

fig.update_layout(template='simple_white')

scatter=fig.data[0]
line = fig.data[1]
colors=['#a3a7e4']*100
scatter.marker.color=colors
scatter.marker.size=[10]*100
fig.layout.hovermode='closest'

fig.update_traces(marker=dict(line=dict(color='DarkSlateGrey')))

out = widgets.Output(layout={'border': '1px solid black'})
out.append_stdout('Output appended with append_stdout\n')

# create our callback function
@out.capture()
def update_point(trace, points, selector):
    x = list(line.x) + points.xs
    y = list(line.y) + points.ys
    line.update(x=x, y=y)
scatter.on_click(update_point)

reset = widgets.Button(description="Reset")
export = widgets.Button(description="Export")

@out.capture()
def on_reset_clicked(b):
    line.update(x=[], y=[])
    out.clear_output()
@out.capture()
def on_export_clicked(b):
    print(fig.to_dict()["data"][1])

reset.on_click(on_reset_clicked)
export.on_click(on_export_clicked)

widgets.VBox([widgets.HBox([reset, export]), widgets.VBox([fig, out])])

fig.show()