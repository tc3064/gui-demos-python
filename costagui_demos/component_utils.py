
import dash
import datajoint as dj
import dash
import dash_table
from dash.dependencies import Input, Output, State
import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import copy
from costagui_demos import dj_utils
from costagui_demos.dj_tables import lab, subject, hardware

table_style_template = dict(
    style_cell={
        'textAlign': 'left',
        'fontSize': 12,
        'font-family': 'helvetica',
        'minWidth': '120px', 'width': '120px', 'maxWidth': '120px',
        'height': '30px'
        },
    page_action='none',
    style_table={
        'minWidth': '1200px',
        'width': '1200px',
        'maxWidth': '1200px',
        'overflowX': 'auto'},
    style_header={
        'backgroundColor': 'rgb(220, 220, 220)',
        'fontWeight': 'bold'})


def create_display_table(table, table_id, height='900px', width='1200px'):

    table_style = copy.deepcopy(table_style_template)
    table_style.update(
        fixed_columns={'headers': True, 'data': 1},
        # allow sorting
        sort_action='native',
        # allow filtering
        filter_action='native',
        # allow selecting a single entry
        row_selectable='single')

    table_style['style_table'].update(
        {
            'minHeight': height,
            'height': height,
            'maxHeight': height,
            'minWidth': width,
            'width': width,
            'maxWidth': width
        }
    )

    return dash_table.DataTable(
        id=table_id,
        columns=[{"name": i, "id": i} for i in table.heading.names],
        data=table.fetch(as_dict=True),
        **table_style
    )


def create_add_record_table(table, table_id, dropdown_fields=[],
                            height='150px', width='1200px',
                            is_update=False):

    table_style = copy.deepcopy(table_style_template)
    table_style['style_table'].update(
        {
            'minHeight': height,
            'height': height,
            'maxHeight': height,
            'minWidth': width,
            'width': width,
            'maxWidth': width
        }
    )

    heading = table.heading
    columns = [{"name": i, "id": i} for i in heading.names]
    # some fields are presented as dropdown list
    if dropdown_fields:
        for c in columns:
            if c['name'] in dropdown_fields:
                c.update(presentation="dropdown")

    if is_update:
        editable = [{c['id']: False}
                    if c['id'] in heading.primary_key else {c['id']: True}
                    for c in columns]
    else:
        editable = True

    return dash_table.DataTable(
        id=table_id,
        columns=columns,
        data=[{c['id']: dj_utils.get_default(table, c['id'])
              for c in columns}],
        **table_style,
        editable=editable,
        dropdown={
            f:
            {
                'options': [{'label': i, 'value': i}
                            for i in dj_utils.get_options(table, f)]
            }
            for f in dropdown_fields
        }
    )


def create_update_modal(table, id, dropdown_fields):

    update_table = create_add_record_table(
        subject.Subject, 'update-' + id + '-table',
        dropdown_fields=dropdown_fields,
        height='200px', width='800x')

    update_message_box = dcc.Textarea(
        id='update-' + id + '-message',
        value='Update message:',
        style={'width': 250, 'height': 200}
    )

    return dbc.Modal(
        [
            dbc.ModalHeader('Update the following record'),
            dbc.Row([dbc.Col(update_table, width=8),
                     dbc.Col(update_message_box, width=4)]),
            dbc.ModalFooter(
                [
                    dbc.Button('Update record', id='update-' + id + '-confirm',
                               className='ml-auto'),
                    dbc.Button('Close', id='close', className='ml-auto')
                ]
            ),
        ],
        id='update-' + id + '-modal',
        size='xl',
    )


def create_filter_dropdown(table, id, field, width='200px'):

    return dcc.Dropdown(
        id=id,
        options=[
            {'label': f, 'value': f} for f in (dj.U(field) & table).fetch(field)
        ],
        style={'width': width, 'marginBottom': '0.5em'},
        placeholder='Select {} ...'.format(field),
    )
