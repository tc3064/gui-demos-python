import datajoint as dj
import dash
import dash_table
from dash.dependencies import Input, Output, State
import dash_html_components as html
import dash_core_components as dcc
import copy

import dash_bootstrap_components as dbc
from dj_tables import hardware
from costagui_demos.app import app
from costagui_demos import dj_utils, component_utils


# ========================= Construct components =========================
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


# ------------------------- hardware table --------------------------------
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

# ------------------------- add hardware table ------------------------------
# some fields are presented as dropdown list
for c in columns:
    if c['name'] in ['sex', 'strain']:
        c.update(presentation="dropdown")

# add hardware table style
add_hardware_style = copy.deepcopy(table_style_template)
add_hardware_style['style_table'].update({
    'minHeight': '100px',
    'height': '100px',
    'maxHeight': '100px',
})

add_hardware_table = dash_table.DataTable(
    id='add-hardware-table',
    columns=columns,
    data=[{c['id']: dj_utils.get_default(hardware.Computer, c['id']) for c in columns}],
    **add_hardware_style,
    editable=True
    )

# ----------------------------- add hardware button ---------------------
add_hardware_button = html.Button(
    children='Add a record',
    id='add-hardware-button', n_clicks=0,
    style={'marginBottom': '0.5em'})

# ------------------------- deletion confirm dialogue -------------------
delete_hardware_confirm = dcc.ConfirmDialog(
    id='delete-hardware-confirm',
    message='Are you sure you want to delete the record?',
)
# ------------------------- deletion hardware button --------------------
delete_hardware_button = html.Button(
    children='Delete the current record',
    id='delete-hardware-button', n_clicks=0,
    style={'marginRight': '1em'})

# ------------------------- update hardware button -----------------------
update_hardware_button = html.Button(
    children='Update the current record',
    id='update-hardware-button', n_clicks=0,
    # style={'display': 'inline-block'}
    )


# ------------------ dropdown menu for hardware options ----------------------

hardware_dropdown = dbc.DropdownMenu(
    [
        dbc.DropdownMenuItem('General Hardware', header=True),
        dbc.DropdownMenuItem('Computer'),
        dbc.DropdownMenuItem('Computer Software'),
        dbc.DropdownMenuItem('Board'),
        dbc.DropdownMenuItem('Camera'),
        dbc.DropdownMenuItem(divider=True),

        dbc.DropdownMenuItem('Scara Hardware', header=True),
        dbc.DropdownMenuItem('Motor'),
        dbc.DropdownMenuItem('Arm'),
        dbc.DropdownMenuItem(divider=True),

        dbc.DropdownMenuItem('Lever Press Hardware', header=True),
        dbc.DropdownMenuItem('Lever'),
        dbc.DropdownMenuItem('Arm'),
        dbc.DropdownMenuItem(divider=True),

        dbc.DropdownMenuItem('Two Photon Hardware', header=True),
        dbc.DropdownMenuItem('Laser'),
        dbc.DropdownMenuItem('Objective'),
        dbc.DropdownMenuItem('Filter'),
        dbc.DropdownMenuItem(divider=True),

        dbc.DropdownMenuItem('Optogenetics Hardware', header=True),
        dbc.DropdownMenuItem('Driver'),
        dbc.DropdownMenuItem('LED'),
    ],
    label='Select table',
    className="mb-3",
)


# ------------------------- hardware tab -------------------------------------
hardware_tab_contents = html.Div(
    children=[
        html.Div(
            # className="row app-body",
            children=[
                html.Div(
                    # Table Selection
                    className="three columns card",
                    children=[
                        hardware_dropdown
                    ],
                    style={'margin-left': '-40px'},
                ),
                # ----------------------------- Tables ---------------------------------
                html.Div(
                    className="eight columns card-left",
                    children=[
                        html.Div(
                            children=[
                                add_hardware_button,
                                add_hardware_table
                            ],
                            style={'marginBottom': '0px'}
                        ),
                        html.Div(
                            children=[
                                delete_hardware_button,
                                update_hardware_button
                            ],
                            style={'marginBottom': '0.5em'}
                        ),
                        hardware_table
                    ],
                    style={'width': '50%', 'marginTop': '-22px'}
                )
            ]
        )
    ]
)
@app.callback(
    # first argument is the id of a component, second is the field of that component
    Output('hardware-table', 'data'), # function returns overwrite the 'data' here
    [Input('add-hardware-button', 'n_clicks'),
     Input('delete-hardware-button', 'n_clicks')],
    [State('add-hardware-table', 'data'),
     State('hardware-table', 'data'),
     State('hardware-table', 'selected_rows')])
# arguments of the call back function need to be the same order
# as the Input and State
def add_hardware(n_clicks_add, n_clicks_delete, new_data, data, selected_rows):
    print(n_clicks_delete)
    ctx = dash.callback_context
    triggered_component = ctx.triggered[0]['prop_id'].split('.')[0]
    print(triggered_component)
    if triggered_component == 'add-hardware-button':
        entry = {k: v for k, v in new_data[0].items() if v!=''}
        hardware.Computer.insert1(entry)
        data = hardware.Computer.fetch(as_dict=True)

    if triggered_component == 'delete-hardware-button' and selected_rows:
        comp = {'computer_name': data[selected_rows[0]]['computer_name']}
        (hardware.Computer & comp).delete()
        data = hardware.Computer.fetch(as_dict=True)

    return data


@app.callback(
    [Output('delete-hardware-button', 'disabled'),
     Output('update-hardware-button', 'disabled')],
    [Input('hardware-table', 'selected_rows')])
def set_button_enabled_state(selected_rows):
    if selected_rows:
        disabled = False
    else:
        disabled = True
    return disabled, disabled

if __name__ == '__main__':

    app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

    app.layout = hardware_tab_contents

    app.run_server(debug=True)
