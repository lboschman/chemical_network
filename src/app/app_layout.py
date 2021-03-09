import dash_core_components as dcc
import dash_html_components as html

def make_layout():
    layout = html.Div([
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

        ]),

        html.Div([

            dcc.RadioItems(
                id='x_axis-type',
                options=[{'label': i, 'value': i} for i in ['Linear', 'Log']],
                value='Linear',
                labelStyle={'display': 'inline-block'}
            )
        ],
            style={'width': '48%', 'display': 'inline-block'}),

        html.Div([

            dcc.RadioItems(
                id='y_axis-type',
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

    return layout
