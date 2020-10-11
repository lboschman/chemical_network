import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State

import plotly.graph_objs as go
import base64
import pandas as pd
import io

import chem_network as cn

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div([
    html.Div([

        html.Div([
            dcc.Upload(id='upload-chemical-system',
                       children=html.Div([
                           'Drag and Drop or ',
                           html.A('Select Files')
                       ]),
                       style={
                           'width': '100%',
                           'height': '60px',
                           'lineHeight': '60px',
                           'borderWidth': '1px',
                           'borderStyle': 'dashed',
                           'borderRadius': '5px',
                           'textAlign': 'center',
                           'margin': '10px'
                       },
                       # Allow multiple files to be uploaded
                       multiple=False
                       ),
            html.Div(id='output-data-upload'),

        ])
        ,

        html.Div([

            dcc.RadioItems(
                id='xaxis-type',
                options=[{'label': i, 'value': i} for i in ['Linear', 'Log']],
                value='Linear',
                labelStyle={'display': 'inline-block'}
            )
        ],
            style={'width': '48%', 'display': 'inline-block'}),

        html.Div([

            dcc.RadioItems(
                id='yaxis-type',
                options=[{'label': i, 'value': i} for i in ['Linear', 'Log']],
                value='Linear',
                labelStyle={'display': 'inline-block'}
            )
        ],
            style={'width': '48%', 'float': 'right', 'display': 'inline-block'})
    ]),

    dcc.Graph(id='indicator-graphic'),

    html.Div(['Lets see what we have here', ]),

    dcc.Checklist(id='plot-compounds', options=[{'label': '', 'value': ''}],
                  # labelStyle={'display': 'inline-block'}
                  ),

    html.Button('OK', id='change-button'),

    dcc.Store(id='reaction-data')

])


@app.callback(
    Output('indicator-graphic', 'figure'),
    [
        Input('xaxis-type', 'value'),
        Input('yaxis-type', 'value'),
        Input('plot-compounds', 'value'),
        Input('reaction-data', 'data')
    ])
def update_graph(xaxis_type, yaxis_type, compound_list, data):
    dff = pd.DataFrame.from_dict(data)

    return {
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
                'type': 'linear' if xaxis_type == 'Linear' else 'log'
            },
            yaxis={
                'title': 'Abundance',
                'type': 'linear' if yaxis_type == 'Linear' else 'log'
            },
            margin={'l': 40, 'b': 40, 't': 10, 'r': 0},
            hovermode='closest'
        )
    }


@app.callback(
    [Output('plot-compounds', 'options'),
     Output('plot-compounds', 'value')],
    [Input('change-button', 'n_clicks'),
     Input('reaction-data', 'data')]
)
def render_compound_checkbox(figure, react_df):
    dff = pd.DataFrame.from_dict(react_df)
    list_dict = [{'label': column, 'value': column} for column in dff.columns]
    col_names = list(dff.columns)
    return list_dict, col_names


def parse_contents(contents, filename):
    content_type, content_string = contents.split(',')

    decoded = base64.b64decode(content_string)
    try:
        if 'csv' in filename:
            # Assume that the user uploaded a CSV file
            df = pd.read_csv(
                io.StringIO(decoded.decode('utf-8')))
        elif 'xls' in filename:
            # Assume that the user uploaded an excel file
            df = pd.read_excel(io.BytesIO(decoded))

        elif 'txt' in filename:
            df = pd.read_fwf(io.StringIO(decoded.decode('utf-8')))

        else:
            raise Exception("File should be xls(x), txt, or csv")

        return df

    except Exception as e:
        print(e)
        return html.Div([
            'There was an error processing this file.'
        ])


@app.callback(Output('reaction-data', 'data'),
              [Input('upload-chemical-system', 'contents'),
               Input('upload-chemical-system', 'filename'),
               ])
def update_reaction_data(contents, filename):
    if contents is None:
        df = pd.read_fwf('../data/test_reactions.txt')
    else:
        df = parse_contents(contents, filename)

    chemical_network = cn.Network()

    for index, row in df.iterrows():
        chemical_network.add_reaction(
            row['Reactants'].split(),
            row['Products'].split(),
            row['Sigma'],
            row['Barrier'],
        )

    # TODO set starting densities via file and or number editors
    # TODO set running time, and time resolution via number editors
    react_df = chemical_network.run_network({'Enzyme': 1, 'Substrate': 10}, t_total=60)
    return react_df.to_dict('records')


if __name__ == '__main__':
    app.run_server(debug=True)
