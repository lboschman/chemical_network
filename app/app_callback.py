import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import dash_table

import plotly.graph_objs as go
import datetime
import base64
import pandas as pd
import io

import chem_network as cn

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

# Create the chemical network

f = open('../data/test_reactions_2.txt', 'r')
lines = f.readlines()
header = lines.pop(0)
reactant_index = 0
product_index = header.index('Products')
sigma_index = header.index('Sigma')
barrier_index = header.index('Barrier')

chemical_network = cn.Network()

for line in lines:
    chemical_network.add_reaction(reactants=line[reactant_index:product_index].split(),
                                  products=line[product_index:sigma_index].split(),
                                  sigma=float(line[sigma_index:barrier_index].strip(' \n')),
                                  barrier=float(line[barrier_index:-1].strip(' \n'))
                                  )

react_df = chemical_network.run_network({'Enzyme': 1, 'Substrate': 10}, t_total=60)

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

])


@app.callback(
    Output('indicator-graphic', 'figure'),
    [
        Input('xaxis-type', 'value'),
        Input('yaxis-type', 'value'),
        Input('plot-compounds', 'value')
    ])
def update_graph(xaxis_type, yaxis_type, compound_list):
    dff = react_df

    # columns = list(dff.columns)
    # cl_scales = cl.scales['{}'.format(len(dff.columns))]['qual']
    # qual_col_keys = cl_scales.keys()
    # color_key = [key for key in qual_col_keys if key[:3]=="Set"]
    # colors = qual_col_keys[color_key[1]]
    # color_dict = {columns[i]: colors[i] for i in range(len(columns))}
    # print(color_dict)

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
    [Input('change-button', 'n_clicks')]
)
def render_compound_checkbox(figure):
    dff = react_df
    list_dict = [{'label': column, 'value': column} for column in dff.columns]
    col_names = list(dff.columns)
    return list_dict, col_names


def parse_contents(contents, filename, date):
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
            lines = decoded
            header = lines.pop(0)
            reactant_index = 0
            product_index = header.index('Products')
            sigma_index = header.index('Sigma')
            barrier_index = header.index('Barrier')
            chemical_network = cn.Network()

            for line in lines:
                chemical_network.add_reaction(reactants=line[reactant_index:product_index].split(),
                                              products=line[product_index:sigma_index].split(),
                                              sigma=float(line[sigma_index:barrier_index].strip(' \n')),
                                              barrier=float(line[barrier_index:-1].strip(' \n'))
                                              )

            react_df = chemical_network.run_network({'Enzyme': 1, 'Substrate': 10}, t_total=60)
            return react_df

    except Exception as e:
        print(e)
        return html.Div([
            'There was an error processing this file.'
        ])

    return html.Div([
        html.H5(filename),
        html.H6(datetime.datetime.fromtimestamp(date)),

        dash_table.DataTable(
            data=df.to_dict('records'),
            columns=[{'name': i, 'id': i} for i in df.columns]
        ),

        html.Hr(),  # horizontal line

        # For debugging, display the raw contents provided by the web browser
        html.Div('Raw Content'),
        html.Pre(contents[0:200] + '...', style={
            'whiteSpace': 'pre-wrap',
            'wordBreak': 'break-all'
        })
    ])


if __name__ == '__main__':
    app.run_server(debug=True)
