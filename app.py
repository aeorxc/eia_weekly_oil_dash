# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Output, Input
from commodplot import commodplot as cpl
import eia
import symbols


external_stylesheets = [dbc.themes.BOOTSTRAP]

app = dash.Dash(__name__, external_stylesheets=external_stylesheets, suppress_callback_exceptions=True)

server = app.server

app.layout = dbc.Container(
    [
        dcc.Store(id="store"),
        dbc.Row(
            [html.H1("EIA: Weekly Petroleum Status Report"),
             html.Plaintext("            Last Update: "),
             dbc.Badge(id='last_update_tag', color="primary", className="ml-1")]),

        html.Hr(),
        html.Div(id='none',children=[],style={'display': 'none'}),
        dbc.Tabs(
            [
                dbc.Tab(label="Overview", tab_id="Overview"),
                # dbc.Tab(label="Crude", tab_id="Crude"),
                # dbc.Tab(label="Gasoline", tab_id="Gasoline"),
                dbc.Tab(label="Config", tab_id="Config"),
            ],
            id="tabs",
            active_tab="Overview",
        ),
        html.Div(id="tab-content", className="p-4"),
    ],
    fluid=True,
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
            if data is None:
                return dcc.Graph()

            return html.Div([
                dbc.Row(
                [
                    dbc.Col(dcc.Graph(figure=data["Crude Stocks"]), width=4),
                    dbc.Col(dcc.Graph(figure=data["Gasoline Stocks"]), width=4),
                    dbc.Col(dcc.Graph(figure=data["Dist Stocks"]), width=4),
                ]),
                dbc.Row(
                [
                    dbc.Col(dcc.Graph(figure=data["Cushing Crude Stocks"]), width=4),
                    dbc.Col(dcc.Graph(figure=data["Gasoline Supplied"]), width=4),
                    dbc.Col(dcc.Graph(figure=data["Dist Fuel Supplied"]), width=4),
                ]),
                dbc.Row(
                [
                    dbc.Col(dcc.Graph(figure=data["Crude Production"]), width=4),
                    dbc.Col(dcc.Graph(figure=data["Refinery Demand"]), width=4),
                    dbc.Col(dcc.Graph(), width=4),
                ]),
            ])
        elif active_tab == "Config":
            return dbc.Row(
                [
                    dbc.Button(
                        "Reset cache",
                        color="primary",
                        block=True,
                        id="reset_cache_button",
                        className="mb-3",
                    ),
                ]
            )
    return "No tab selected"


@app.callback(Output("store", "data"),  [Input('none', 'children')])
def generate_graphs(none):

    df = eia.get_symbols(tuple(symbols.basic.values()))
    df = df.tail(12*52)
    res = {}
    yaxt = 'mb'

    for item, symbol in symbols.basic.items():
        res[item] = cpl.seas_line_plot(df[symbol]/1000, title=item, histfreq='W', shaded_range=5, yaxis_title=yaxt)

    # save figures in a dictionary for sending to the dcc.Store
    return res


@app.callback(Output("none", "children"), [Input("reset_cache_button", "n_clicks")])
def reset_cache_button(n):
    eia.clear_cache()


@app.callback(Output("last_update_tag", "children"), [Input("none", "n_clicks")])
def last_update_tag(n_clicks):
    return eia.last_update_tag()


if __name__ == '__main__':
    app.run_server(debug=True)
