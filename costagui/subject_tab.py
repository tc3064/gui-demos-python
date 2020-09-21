import datajoint as dj
import dash
import dash_table
from dash.dependencies import Input, Output, State
import dash_html_components as html
import dash_core_components as dcc
import copy

from dj_tables import lab, subject, hardware
import utils

## ========================= Construct components =========================
# table style settings
table_style_template = dict(
    fixed_columns={'headers': True, 'data': 1},
    style_cell={
        'textAlign': 'left',
        'fontSize':12,
        'font-family':'helvetica',
        'minWidth': '120px', 'width': '120px', 'maxWidth': '120px',
        'overflow': 'hidden',
        'height': '30px'},
    page_action='none',
    style_table={
        'minWidth': '1200px',
        'width': '1200px',
        'maxWidth': '1200px',
        'overflowY': 'scroll',
        'overflowX': 'scroll'},
    style_header={
        'backgroundColor': 'rgb(220, 220, 220)',
        'fontWeight': 'bold'})


## ------------------------- subject table --------------------------------
# subject table style
subject_table_style = copy.deepcopy(table_style_template)
subject_table_style.update(
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

subject_table_style['style_table'].update({
    'minHeight': '900px',
    'height': '900px',
    'maxHeight': '900px',
})

# from datajoint tables, get the data and table definition
subjs = subject.Subject.fetch(as_dict=True)
columns = [{"name": i, "id": i} for i in subject.Subject.heading.names]

subject_table = dash_table.DataTable(
    id='subject-table',
    columns=columns,
    data=subjs,
    # below are all styles
    **subject_table_style
)

## ------------------------- add subject table ------------------------------
# some fields are presented as dropdown list
for c in columns:
    if c['name'] in ['sex', 'strain']:
        c.update(presentation="dropdown")

# add subject table style
add_subject_style = copy.deepcopy(table_style_template)
add_subject_style['style_table'].update({
    'minHeight': '150px',
    'height': '150px',
    'maxHeight': '150px',
})

add_subject_table = dash_table.DataTable(
    id='add-subject-table',
    columns=columns,
    data=[{c['id']: utils.get_default(subject.Subject, c['id']) for c in columns}],
    **add_subject_style,
    editable=True,
    dropdown={
        'sex': {
            'options': [{'label': i, 'value': i} for i in utils.get_options(subject.Subject, 'sex')]
        },
        'subject_strain': {
            'options': [{'label': i, 'value': i} for i in utils.get_options(subject.Subject, 'subject_strain')]
        }
    })

## ----------------------------- add subject button ---------------------------------
add_subject_button = html.Button(
    children='Add a subject record',
    id='add-subject-button', n_clicks=0,
    style={'marginBottom': '0.5em'})

## ------------------------- deletion confirm dialogue ------------------------------
delete_subject_confirm = dcc.ConfirmDialog(
    id='delete-subject-confirm',
    message='Are you sure you want to delete the record?',
),
## ------------------------- deletion subject button --------------------------------
delete_subject_button = html.Button(
    children='Delete the current record',
    id='delete-subject-button', n_clicks=0,
    style={'marginRight': '1em'})

## ------------------------- update subject button --------------------------------
update_subject_button = html.Button(
    children='Update the current record',
    id='update-subject-button', n_clicks=0,
    # style={'display': 'inline-block'}
    )


## ------------------------- subject tab -------------------------------------
subject_tab_contents = html.Div(
    html.Div(
        className="row app-body",
        children=[
            add_subject_button,
            add_subject_table,
            html.Div(
                [
                    delete_subject_button,
                    update_subject_button
                ],
                style={'marginBottom': '0.5em'}),
            html.Div([subject_table],
                style={'marginBottom': '1em'}),
        ]

    )
)
