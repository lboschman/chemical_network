import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

import plotly.graph_objs as go

import chem_network as cn

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

# Create the chemical network

f = open('../data/test_reactions.txt', 'r')
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

    # dcc.Checklist(id='plot-')


])

@app.callback(
    Output('indicator-graphic', 'figure'),
    [
         # Input('xaxis-column', 'value'),
         # Input('yaxis-column', 'value'),
         Input('xaxis-type', 'value'),
         Input('yaxis-type', 'value'),
         # Input('year--slider', 'value')
])
def update_graph(xaxis_type, yaxis_type):
    dff = react_df

    return {
        'data': [go.Scatter(
            x=dff.index,
            y=dff[column_name],
            text=column_name,
            mode='lines',
            name=column_name

        ) for column_name in dff.columns],
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


if __name__ == '__main__':
    app.run_server(debug=True)