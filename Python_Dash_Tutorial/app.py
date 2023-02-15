from dash import Dash, html, dcc
import plotly.express as px
import pandas as pd

app_teste = Dash(__name__)

colors = {
    'background': '#111111',
    'text': '#7FDBFF'
}

df = pd.DataFrame({
    "Fruit": ["Apple", "Oranges", "Bananas", "Apples", "Oranges", "Bananas"],
    "Amount": [4, 1, 2, 2, 4, 5],
    "City": ["SF", "SF", "SF", "Montreal", "Montreal", "Montreal"]
    })

fig = px.bar(df, x="Fruit", y="Amount", color="City", barmode="group")

fig.update_layout(
    plot_bgcolor=colors['background'],
    paper_bgcolor=colors['background'],
    font_color=colors['text']
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