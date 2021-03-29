from entsoe import EntsoePandasClient
#from keys import ENTSOE_API_KEY
import plotly.express as px
import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
from datetime import date, timedelta
import os

ENTSOE_API_KEY = os.environ['ENTSOE_API_KEY']

# start = pd.Timestamp(f"{today.year}{str(today.month).zfill(2)}01")
# end = pd.Timestamp(f"{today.year}{str(today.month).zfill(2)}{str(today.day).zfill(2)}")
# zones = ['NL', 'AT', 'DE_LU', 'BE', 'FR']


def get_dayahead_prices_fig(zones, start, end):
    client = EntsoePandasClient(api_key=ENTSOE_API_KEY)
    data = {}
    for zone in zones:
        data[zone]=client.query_day_ahead_prices(zone, start=start, end=end)
    df = pd.DataFrame(data)
    fig = px.line(df, line_shape='hv', labels={'index': 'time', 'value': 'Price [EUR / MWh]'})
    return fig

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

server = app.server


app.layout = html.Div(children=[
    html.H1(children='CWE Day Ahead market prices'),
    html.Div(children='Please select a date range'),
    html.Div(children=[dcc.DatePickerRange(
        id='date-picker-range',
        min_date_allowed=date(2014, 1, 1),
        max_date_allowed=date(date.today().year, 12, 31),
        initial_visible_month=date.today(),
        end_date=date.today()+timedelta(days=1)
    )]),
    html.Button('Fetch', id='btn-fetch', n_clicks=0),
    html.Div([dcc.Graph(id='prices-day-ahead')])
])


@app.callback(
    dash.dependencies.Output('prices-day-ahead', 'figure'),
    [dash.dependencies.Input('btn-fetch', 'n_clicks')],
    [dash.dependencies.State('date-picker-range', 'start_date'), dash.dependencies.State('date-picker-range', 'end_date')])
def update_graph(n_clicks, start_date, end_date):
    if start_date is not None and end_date is not None:
        return get_dayahead_prices_fig(['NL', 'AT', 'DE_LU', 'BE', 'FR'],
                                       pd.Timestamp(start_date), pd.Timestamp(end_date))
    return {}


if __name__ == '__main__':
    app.run_server(debug=True)