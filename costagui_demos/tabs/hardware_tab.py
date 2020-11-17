import datajoint as dj
import dash
import dash_table
from dash.dependencies import Input, Output, State
import dash_html_components as html
import dash_core_components as dcc
import copy

import dash_bootstrap_components as dbc
from costagui_demos.dj_tables import hardware
from costagui_demos.app import app
from costagui_demos import dj_utils, component_utils

width = '900px'
height = '200px'

hardware_table = component_utils.create_display_table(
    hardware.Computer, 'hardware-table', width=width
)

# ------------------------- add hardware table ------------------------------
add_hardware_table = component_utils.create_edit_record_table(
    hardware.Computer, 'add-hardware-table', width=width,
    height=height
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
    id='update-hardware-button', n_clicks=0
)


# ------------------ dropdown menu for hardware options ----------------------

hardware_dropdown = dbc.DropdownMenu(
    [
        dbc.DropdownMenuItem('General Hardware', header=True),
        dbc.DropdownMenuItem('Computer', id='computer-menu-item'),
        dbc.DropdownMenuItem('Computer Software', id='software-menu-item'),
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
            className="row app-body",
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
                                html.Div(
                                    add_hardware_table,
                                    id='current-add-hardware-table')
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
                        html.Div(
                            hardware_table,
                            id='current-hardware-table',
                        )
                    ],
                    style={'width': '50%', 'marginTop': '-22px'}
                ),
                # hidden variable for the current table
                html.Div(id='current-table', style={'display': 'none'},
                         children='computer-menu-item')
            ]
        )
    ]
)

tables = {
    'computer-menu-item': hardware.Computer,
    'software-menu-item': hardware.Computer.InstalledSoftware
}


# update the current table based on the selected menu item
@app.callback(
    [Output('current-table', 'children'),
     Output('current-hardware-table', 'children'),
     Output('current-add-hardware-table', 'children')],
    [Input(t, 'n_clicks') for t in tables.keys()],
)
def update_current_table(*args):
    ctx = dash.callback_context
    triggered_component = ctx.triggered[0]['prop_id'].split('.')[0]
    print(triggered_component)

    if triggered_component:
        current_table = tables[triggered_component]

        return triggered_component, \
            component_utils.create_display_table(
                current_table, 'hardware-table', width=width
            ), \
            component_utils.create_edit_record_table(
                current_table, 'add-hardware-table', width=width,
                height=height
            )
    else:
        return 'computer-menu-item', \
            component_utils.create_display_table(
                hardware.Computer, 'hardware-table', width=width
            ), \
            component_utils.create_edit_record_table(
                hardware.Computer, 'add-hardware-table', width=width,
                height=height
            )


@app.callback(
    # first argument is the id of a component, second is the field of that component
    Output('hardware-table', 'data'),
    [Input('add-hardware-button', 'n_clicks'),
     Input('delete-hardware-button', 'n_clicks')],
    [State('current-table', 'children'),
     State('add-hardware-table', 'data'),
     State('hardware-table', 'data'),
     State('hardware-table', 'selected_rows')])
# arguments of the call back function need to be the same order
# as the Input and State
def add_hardware(n_clicks_add, n_clicks_delete,
                 current_menu_item, new_data, data, selected_rows):

    current_table = tables[current_menu_item]

    ctx = dash.callback_context
    triggered_component = ctx.triggered[0]['prop_id'].split('.')[0]

    if triggered_component == 'add-hardware-button':
        entry = {k: v for k, v in new_data[0].items() if v != ''}
        current_table.insert1(entry)
        data = current_table.fetch(as_dict=True)

    if triggered_component == 'delete-hardware-button' and selected_rows:
        pks = current_table.heading.primary_key
        comp = {pk: data[selected_rows[0]][pk] for pk in pks}
        if isinstance(current_table(), dj.Part):
            (current_table & comp).delete(force=True)
        else:
            (current_table & comp).delete()
        data = current_table.fetch(as_dict=True)

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

    dj.config['safemode'] = False

    app.layout = hardware_tab_contents

    app.run_server(debug=True)
