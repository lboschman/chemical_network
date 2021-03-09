#!/usr/bin/env python

import dash
from dash.dependencies import Input, Output
from dash.exceptions import PreventUpdate

import plotly.graph_objs as go
import pandas as pd

from ..engine import chem_network as cn

from .app_layout import make_layout
from .helpers import parse_contents

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.layout = make_layout()


@app.callback(
    Output('indicator-graphic', 'figure'),
    [
        Input('x_axis-type', 'value'),
        Input('y_axis-type', 'value'),
        Input('plot-compounds', 'value'),
        Input('reaction-data', 'data')
    ])
def update_graph(x_axis_type, y_axis_type, compound_list, data):
    """Update the plotted graph"""
    dff = pd.DataFrame.from_dict(data)

    return {
        # Make data points for every selected compound
        'data': [go.Scatter(
            x=dff.index,
            y=dff[column_name],
            text=column_name,
            mode='lines',
            name=column_name,
            # line=dict(color=color_dict[column_name])

        ) for column_name in compound_list],
        'layout': go.Layout(
            xaxis={
                'title': 'Time',
                'type': 'linear' if x_axis_type == 'Linear' else 'log'
            },
            yaxis={
                'title': 'Abundance',
                'type': 'linear' if y_axis_type == 'Linear' else 'log'
            },
            margin={'l': 40, 'b': 40, 't': 10, 'r': 0},
            hovermode='closest'
        )
    }


@app.callback(
    [Output('plot-compounds', 'options'),
     Output('plot-compounds', 'value')],
    [Input('reaction-data', 'data')]
)
def render_compound_checkbox(react_df):
    """Create the compound checkbox.

    This checkbox helps remove lines for clarity in the simulation plot.
    """
    if react_df is None:
        raise PreventUpdate
    dff = pd.DataFrame.from_dict(react_df)
    # Create labels from the column names in the reaction dataframe
    list_dict = [{'label': column, 'value': column} for column in dff.columns]
    col_names = list(dff.columns)
    return list_dict, col_names


@app.callback(Output('reaction-data', 'data'),
              [Input('upload-chemical-system', 'contents'),
               Input('upload-chemical-system', 'filename'),
               ])
def update_reaction_data(contents, filename):
    """Read a file, initiate a chemical network, and run the network.

    Output data is stored in a DataFrame, and then stored in a dcc.Store object.
    """
    if contents is None:
        df = pd.read_fwf('../data/test_reactions.txt')
    else:
        df = parse_contents(contents, filename)

    # Initiate chemical network
    chemical_network = cn.Network()

    # Add individual reactions to the network
    for index, row in df.iterrows():
        chemical_network.add_reaction(
            row['Reactants'].split(),
            row['Products'].split(),
            row['Sigma'],
            row['Barrier'],
        )

    # TODO set starting densities via file and or number editors
    # TODO set running time, and time resolution via number editors
    # Let the network run for a predetermined amount of time
    react_df = chemical_network.run_network({'Enzyme': 1, 'Substrate': 10}, t_total=60)
    return react_df.to_dict('records')


if __name__ == '__main__':
    app.run_server(debug=True)
