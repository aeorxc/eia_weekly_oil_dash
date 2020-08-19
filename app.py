# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Output, Input
from commodplot import commodplot as cpl
import eia


external_stylesheets = [dbc.themes.BOOTSTRAP]

app = dash.Dash(__name__, external_stylesheets=external_stylesheets, suppress_callback_exceptions=True)

server = app.server

app.layout = dbc.Container(
    [
        dcc.Store(id="store"),
        html.H1("EIA: Weekly Petroleum Status Report"),
        html.Hr(),
        html.Div(id='none',children=[],style={'display': 'none'}),
        dbc.Tabs(
            [
                dbc.Tab(label="Overview", tab_id="Overview"),
                dbc.Tab(label="Crude", tab_id="Crude"),
                dbc.Tab(label="Gasoline", tab_id="Gasoline"),
            ],
            id="tabs",
            active_tab="Overview",
        ),
        html.Div(id="tab-content", className="p-4"),
    ]
)


@app.callback(
    Output("tab-content", "children"),
    [Input("tabs", "active_tab"), Input("store", "data")],
)
def render_tab_content(active_tab, data):
    """
    This callback takes the 'active_tab' property as input, as well as the
    stored graphs, and renders the tab content depending on what the value of
    'active_tab' is.
    """
    if active_tab:
        if active_tab == "Overview":
            return dbc.Row(
                [
                    dbc.Col(dcc.Graph(figure=data["crude_stocks"]), width=4),
                    dbc.Col(dcc.Graph(figure=data["gasoline_stocks"]), width=4),
                    dbc.Col(dcc.Graph(figure=data["dist_stocks"]), width=4),
                ]
            )
        elif active_tab == "Crude":
            return dbc.Row(
                [
                    dbc.Col(dcc.Graph(), width=6),
                    dbc.Col(dcc.Graph(), width=6),
                ]
            )
    return "No tab selected"


@app.callback(Output("store", "data"),  [Input('none', 'children')])
def generate_graphs(none):

    df = eia.overview()
    df = df.tail(12*52)
    res = {}
    res['crude_stocks'] = cpl.seas_line_plot(df['PET.WCESTUS1.W']/100, title='Crude Stocks', histfreq='W', shaded_range=5)
    res['gasoline_stocks'] = cpl.seas_line_plot(df['PET.WGTSTUS1.W']/100, title='Gasoline Stocks', histfreq='W', shaded_range=5)
    res['dist_stocks'] = cpl.seas_line_plot(df['PET.WDISTUS1.W']/100, title='Dist Stocks', histfreq='W', shaded_range=5)

    # save figures in a dictionary for sending to the dcc.Store
    return res


if __name__ == '__main__':
    app.run_server(debug=True)
