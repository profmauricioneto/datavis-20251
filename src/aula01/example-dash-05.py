from dash import Dash, dcc, html, Output, Input, callback
import plotly.express as px
import pandas as pd

app = Dash(__name__)

app.layout = html.Div([
   html.H5("Example of Callbacks!"),
   html.P("Change de value in text box: "),
   html.Div([
       'Input: ',
       dcc.Input(id='text-value', type='text', placeholder='digite algo...')
   ]),
   html.Br(),
   html.Div(id='output-value'),
])
@callback(
   Output(component_id='output-value', component_property='children'),
   Input(component_id='text-value', component_property='value')
)
def update_output(value):
   return f'Output: {value}'

if __name__ == '__main__':
   app.run(debug=True)