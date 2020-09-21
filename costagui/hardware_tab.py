import datajoint as dj
import dash
import dash_table
from dash.dependencies import Input, Output, State
import dash_html_components as html
import dash_core_components as dcc
import copy

import dash_bootstrap_components as dbc
from dj_tables import hardware
import utils


## ========================= Construct components =========================
# table style settings
table_style_template = dict(
    fixed_columns={'headers': True, 'data': 1},
    style_cell={
        'textAlign': 'left',
        'fontSize':12,
        'font-family':'helvetica',
        'minWidth': '150px', 'width': '150px', 'maxWidth': '150px',
        'overflow': 'hidden',
        'height': '30px'},
    page_action='none',
    style_table={
        'minWidth': '950px',
        'width': '950px',
        'maxWidth': '950px',
        'overflowY': 'scroll',
        'overflowX': 'scroll'},
    style_header={
        'backgroundColor': 'rgb(220, 220, 220)',
        'fontWeight': 'bold'})


## ------------------------- hardware table --------------------------------
# hardware table style
hardware_table_style = copy.deepcopy(table_style_template)
hardware_table_style.update(
    style_data_conditional=[
        {'if': {'row_index': 'odd'},
        'backgroundColor': 'rgb(245, 245, 245)'}
    ],
    # allow sorting
    sort_action='native',
    # allow filtering
    filter_action='native',
    # allow selecting a single entry
    row_selectable='single')

hardware_table_style['style_table'].update({
    'minHeight': '600px',
    'height': '600px',
    'maxHeight': '600px',
})

# from datajoint tables, get the data and table definition
comp = hardware.Computer.fetch(as_dict=True)
columns = [{"name": i, "id": i} for i in hardware.Computer.heading.names]

hardware_table = dash_table.DataTable(
    id='hardware-table',
    columns=columns,
    data=comp,
    # below are all styles
    **hardware_table_style
)

## ------------------------- add hardware table ------------------------------
# some fields are presented as dropdown list
for c in columns:
    if c['name'] in ['sex', 'strain']:
        c.update(presentation="dropdown")

# add subject table style
add_hardware_style = copy.deepcopy(table_style_template)
add_hardware_style['style_table'].update({
    'minHeight': '200px',
    'height': '200px',
    'maxHeight': '200px',
})

add_hardware_table = dash_table.DataTable(
    id='add-hardware-table',
    columns=columns,
    data=[{c['id']: utils.get_default(hardware.Computer, c['id']) for c in columns}],
    **add_hardware_style,
    editable=True
    # dropdown={
    #     'sex': {
    #         'options': [{'label': i, 'value': i} for i in utils.get_options(subject.Subject, 'sex')]
    #     },
    #     'subject_strain': {
    #         'options': [{'label': i, 'value': i} for i in utils.get_options(subject.Subject, 'subject_strain')]
    #     }
    #}
    )

## ----------------------------- add subject button ---------------------------------
add_hardware_button = html.Button(
    children='Add a record',
    id='add-hardware-button', n_clicks=0,
    style={'marginBottom': '0.5em'})

## ------------------------- deletion confirm dialogue ------------------------------
delete_hardware_confirm = dcc.ConfirmDialog(
    id='delete-hardware-confirm',
    message='Are you sure you want to delete the record?',
)
## ------------------------- deletion subject button --------------------------------
delete_hardware_button = html.Button(
    children='Delete the current record',
    id='delete-hardware-button', n_clicks=0,
    style={'marginRight': '1em'})

## ------------------------- update subject button --------------------------------
update_hardware_button = html.Button(
    children='Update the current record',
    id='update-hardware-button', n_clicks=0,
    # style={'display': 'inline-block'}
    )

## ------------------------- hardware tab -------------------------------------
hardware_tab_contents = html.Div(
    children=[
        html.Div(
            className="row app-body",
            children=[

            html.Div(
                #Table Selection
                className="three columns card",
                children=[
                ## ----------------------------- Table Options ---------------------------------
                    html.Div(
                        className="bg-white user-control",
                        children=[
                            html.Div(
                                children=[
                                    ## ----------------------------- General Hardware ---------------------------------
                                    html.Div(
                                        className="padding-bot",
                                        children= [
                                            html.H6("General Hardware"),
                                            dcc.Dropdown(
                                            id='general-hardware-dropdown',
                                            options=[
                                                # label is what is shown up on the dropdown list
                                                {'label': 'Computer', 'value': 'Computer'},
                                                {'label': 'Computer Software', 'value': 'InstalledSoftware'},
                                                {'label': 'Board', 'value': 'Board'},
                                                {'label': 'Camera', 'value': 'Camera'},
                                            ],
                                            # value='U',
                                            style={'width': '200px'},
                                            # clearable=False,
                                            # searchable=False,
                                            multi=False,
                                            placeholder='Select table ...')
                                        ]
                                    ),
                                    ## ----------------------------- Scara Hardware ---------------------------------
                                    html.Div(
                                        className="padding-top-bot",
                                        children=[
                                            html.H6("Scara Hardware"),
                                            dcc.Dropdown(
                                            id='scara-hardware-dropdown',
                                            options=[
                                                # label is what is shown up on the dropdown list
                                                {'label': 'Motor', 'value': 'Motor'},
                                                {'label': 'Arm', 'value': 'Arm'},
                                            ],
                                            # value='U',
                                            style={'width': '200px'},
                                            # clearable=False,
                                            # searchable=False,
                                            multi=False,
                                            placeholder='Select table ...')
                                        ]
                                    ),


                                    ## ----------------------------- Lever Press Hardware ---------------------------------
                                    html.Div(
                                        className="padding-top-bot",
                                        children=[
                                            html.H6("Lever Press Hardware"),
                                            dcc.Dropdown(
                                            id='leverpress-hardware-dropdown',
                                            options=[
                                                # label is what is shown up on the dropdown list
                                                {'label': 'Lever', 'value': 'Lever'},
                                                {'label': 'Arm', 'value': 'Arm'},
                                            ],
                                            # value='U',
                                            style={'width': '200px'},
                                            # clearable=False,
                                            # searchable=False,
                                            multi=False,
                                            placeholder='Select table ...')
                                        ]
                                    ),

                                    ## ----------------------------- 2p Hardware ---------------------------------
                                    html.Div(
                                        className="padding-top-bot",
                                        children=[
                                            html.H6("Two Photon Hardware"),
                                            dcc.Dropdown(
                                            id='twophoton-hardware-dropdown',
                                            options=[
                                                # label is what is shown up on the dropdown list
                                                {'label': 'Laser', 'value': 'Laser'},
                                                {'label': 'Objective', 'value': 'Objective'},
                                                {'label': 'Filter', 'value': 'Filter'},
                                            ],
                                            # value='U',
                                            style={'width': '200px'},
                                            # clearable=False,
                                            # searchable=False,
                                            multi=False,
                                            placeholder='Select table ...')
                                        ]
                                    ),

                                    ## ----------------------------- Optogenetics Hardware ---------------------------------
                                    html.Div(
                                        className="padding-top-bot",
                                        children=[
                                            html.H6("Optogenetics Hardware"),
                                            dcc.Dropdown(
                                            id='optogenetics-hardware-dropdown',
                                            options=[
                                                # label is what is shown up on the dropdown list
                                                {'label': 'Driver', 'value': 'OptoDriver'},
                                                {'label': 'LED', 'value': 'OptoLED'},
                                            ],
                                            # value='U',
                                            style={'width': '200px'},
                                            # clearable=False,
                                            # searchable=False,
                                            multi=False,
                                            placeholder='Select table ...')
                                        ]
                                    )
                                ],
                            ),
                        ],
                    )
                ],
                style={'margin-left': '-40px'},
            ),
            ## ----------------------------- Tables ---------------------------------
            html.Div(
                className="eight columns card-left",
                children=[
                    html.Div(
                        children =
                        [
                            add_hardware_button,
                            add_hardware_table
                        ],
                        style={'marginBottom': '-90px'}
                    ),

                    html.Div(
                        children =
                        [
                            delete_hardware_button,
                            update_hardware_button
                        ],
                        style={'marginBottom': '0.5em'}
                    ),
                    hardware_table
                ],
                style={'width': '50%', 'marginTop': '-22px'}
            )
## -----------------------------------------------------------------------------
          ]
        )
    ]
)
