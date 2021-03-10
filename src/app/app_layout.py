import dash_core_components as dcc
import dash_html_components as html

def build_file_upload():

    return html.Div(
        id="file-upload",
        className="file-upload",
        children=[
            dcc.Upload(
                id='upload-chemical-system',
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
            )
        ]
    )


def build_axis_scale_toggles():
    # TODO replace the radio buttons with a toggleswitch
    # https://dash.plotly.com/dash-daq/toggleswitch
    return html.Div(
        id="scale-toggles",
        children=[
            html.Div(
                id='x-axis-toggle',
                children=[
                    dcc.RadioItems(
                        id='x_axis-type',
                        options=[{'label': i, 'value': i} for i in ['Linear', 'Log']],
                        value='Linear',
                        labelStyle={'display': 'inline-block'}
                    )
                ],
                style={'width': '48%', 'display': 'inline-block',}
            ),

            html.Div(
                id='y-axis-toggle',
                children=[
                    dcc.RadioItems(
                        id='y_axis-type',
                        options=[{'label': i, 'value': i} for i in ['Linear', 'Log']],
                        value='Linear',
                        labelStyle={'display': 'inline-block'}
                    )
                ],
                style={'width': '48%', 'float': 'right', 'display': 'inline-block'}
            )
        ]
    )



def build_banner():
    # This function was repurposed from 
    # https://github.com/plotly/dash-sample-apps/blob/master/apps/dash-manufacture-spc-dashboard/app.py
    return html.Div(
        id="banner",
        className="banner",
        children=[
            html.Div(
                id="banner-text",
                children=[
                    html.H5("Chemical Reactions"),
                    # html.H6(""),
                ],
            ),
            html.Div(
                id="banner-logo",
                children=[
                    html.Button(
                        id="learn-more-button", children="LEARN MORE", n_clicks=0
                    ),
                    # html.Img(id="logo", src=app.get_asset_url("dash-logo-new.png")),
                ],
            ),
        ],
    )


def make_layout():
    layout = html.Div(
        id='big-app-container',
        children=[
            # TODO make the banner look nicer
            build_banner(),
            # TODO make tabs: 
            # 1) with settings 
            # 2) with table with reactions 
            # 3) with graph and output and stuff
            html.Div([

                build_file_upload(),

                build_axis_scale_toggles(),
            ]),

            dcc.Graph(id='indicator-graphic'),

            html.Div(['Lets see what we have here', ]),

            dcc.Checklist(id='plot-compounds', options=[{'label': '', 'value': ''}],
                        # labelStyle={'display': 'inline-block'}
                        ),

            html.Button('OK', id='change-button'),

            dcc.Store(id='reaction-data'),
        ]
    )

    return layout
