import datajoint as dj
import dash
from dash.dependencies import Input, Output
import dash_html_components as html
import dash_bootstrap_components as dbc
from costagui_demos.app import app
from costagui_demos.dj_tables import lab, hardware
from dj_dashboard.templates import TableBlock


# Add all the tabs needed here.
hardware_block = TableBlock(hardware.Computer, app)
software_block = TableBlock(hardware.Computer.InstalledSoftware, app)
board_block = TableBlock(hardware.Board, app)

table_layouts = {
    'computer-menu-item': hardware_block.layout,
    'software-menu-item': software_block.layout,
    'board-menu-item': board_block.layout,
}

hardware_dropdown = dbc.DropdownMenu(
    [
        dbc.DropdownMenuItem('General Hardware', header=True),
        dbc.DropdownMenuItem('Computer', id='computer-menu-item'),
        dbc.DropdownMenuItem('Computer Software', id='software-menu-item'),
        dbc.DropdownMenuItem('Board', id='board-menu-item'),
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

hardware_tab_contents = html.Div(
            className="row app-body",
            children=[
                html.Div(
                    # Table Selection
                    className="two columns card",
                    children=[
                        hardware_dropdown
                    ],
                    style={'margin-left': '-40px'},
                ),
                html.Div(
                    id='hardware-layout',
                    children=hardware_block.layout
                ),
                # hidden variable for the current table
                html.Div(id='current-table', style={'display': 'none'},
                         children='computer-menu-item')
            ]
        )


# update the current table based on the selected menu item
@app.callback(
    [Output('hardware-layout', 'children')],
    [Input(t, 'n_clicks') for t in table_layouts.keys()],
)
def update_tab(*args):
    ctx = dash.callback_context
    triggered_component = ctx.triggered[0]['prop_id'].split('.')[0]

    if triggered_component:
        return [table_layouts[triggered_component]]
    else:
        return [hardware_block.layout]


if __name__ == '__main__':
    dj.config['safemode'] = False
    app.layout = hardware_tab_contents
    app.run_server(debug=True)
