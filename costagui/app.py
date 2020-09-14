import datajoint as dj
import dash
import dash_table
from dash.dependencies import Input, Output, State
import dash_html_components as html
import dash_core_components as dcc
import copy

from dj_tables import lab, subject
import utils

## ========================= Create a flask app ===========================
# dash does the job for you
app = dash.Dash(__name__)


## ========================= Construct components =========================
# table style settings
table_style_template = dict(
    fixed_columns={'headers': True, 'data': 1},
    style_cell={
        'textAlign': 'left',
        'fontSize':12,
        'font-family':'helvetica',
        'minWidth': '80px', 'width': '80px', 'maxWidth': '130px',
        'overflow': 'hidden',
        'height': '30px'},
    page_action='none',
    style_table={
        'minWidth': '700px',
        'width': '700px',
        'maxWidth': '700px',
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
    'minHeight': '600px',
    'height': '600px',
    'maxHeight': '600px',
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
    if c['name'] in ['sex', 'subject_line']:
        c.update(presentation="dropdown")

# add subject table style
add_subject_style = copy.deepcopy(table_style_template)
add_subject_style['style_table'].update({
    'minHeight': '200px',
    'height': '200px',
    'maxHeight': '200px',
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
        'subject_line': {
            'options': [{'label': i, 'value': i} for i in utils.get_options(subject.Subject, 'subject_line')]
        }
    })

## ----------------------------- add subject button ---------------------------------
add_subject_button = html.Button(
    children='Add a subject record',
    id='add-subject-button', n_clicks=0,
    style={'marginBottom': '0.5em'})


## ----------------------------- subject users table ----------------------------------
subject_users_columns = [
    {"name": i, "id": i} for i in subject.Subject.User.heading.names]
subject_users_style = copy.deepcopy(add_subject_style)
subject_users_style.update(
    style_table = {
        'minWidth': '250px',
        'width': '250px',
        'maxWidth': '250px',
        'minHeight': '200px',
        'height': '200px',
        'maxHeight': '200px',
        'overflowY': 'scroll',
        'overflowX': 'scroll'},
)
subject_users_table = dash_table.DataTable(
    id='subject-users-table',
    columns=subject_users_columns,
    data=[{c['id']: '' for c in subject_users_columns}],
    **subject_users_style,
)

## ----------------------------- subject protocols table -------------------------------
subject_protocols_columns = [
    {"name": i, "id": i} for i in subject.Subject.Protocol.heading.names]
subject_protocols_style = copy.deepcopy(add_subject_style)
subject_protocols_style.update(
    style_table = {
        'minWidth': '300px',
        'width': '300px',
        'maxWidth': '300px',
        'minHeight': '200px',
        'height': '200px',
        'maxHeight': '200px',
        'overflowY': 'scroll',
        'overflowX': 'scroll'},
)
subject_protocols_table = dash_table.DataTable(
    id='subject-protocols-table',
    columns=subject_protocols_columns,
    data=[{c['id']: '' for c in subject_protocols_columns}],
    **subject_protocols_style,
)

## ----------------------------- add subject users table ------------------------------

for c in subject_users_columns:
    if c['name'] in ['user']:
        c.update(presentation="dropdown")

add_subject_users_style = copy.deepcopy(add_subject_style)
add_subject_users_style.update(
    style_table = {
        'minWidth': '250px',
        'width': '250px',
        'maxWidth': '250px',
        'minHeight': '200px',
        'height': '200px',
        'maxHeight': '200px',
        'overflowY': 'scroll',
        'overflowX': 'scroll'},
)
unit_data = {c['id']: utils.get_default(subject.Subject.User, c['id'])
             for c in subject_users_columns}
add_subject_users_table = dash_table.DataTable(
    id='add-subject-users-table',
    columns=subject_users_columns,
    data=[unit_data] * 3,
    **add_subject_users_style,
    editable=True,
    dropdown={
        'user': {
            'options': [{'label': i, 'value': i} for i in utils.get_options(subject.Subject.User, 'user')]
        },
    })

## ------------------------- add subject users button -------------------------------
add_subject_users_button = html.Button(
    children='Add subject users',
    id='add-subject-users-button', n_clicks=0,
    style={'marginBottom': '0.5em'})

## ----------------------------- add subject protocols table ------------------------------
subject_protocols_columns = [
    {"name": i, "id": i} for i in subject.Subject.Protocol.heading.names]

for c in subject_protocols_columns:
    if c['name'] in ['protocol']:
        c.update(presentation="dropdown")

add_subject_protocols_style = copy.deepcopy(add_subject_style)
add_subject_protocols_style.update(
    style_table = {
        'minWidth': '300px',
        'width': '300px',
        'maxWidth': '300px',
        'minHeight': '200px',
        'height': '200px',
        'maxHeight': '200px',
        'overflowY': 'scroll',
        'overflowX': 'scroll'},
)
unit_data = {c['id']: utils.get_default(subject.Subject.Protocol, c['id'])
             for c in subject_protocols_columns}
add_subject_protocols_table = dash_table.DataTable(
    id='add-subject-protocols-table',
    columns=subject_protocols_columns,
    data=[unit_data] * 3,
    **add_subject_protocols_style,
    editable=True,
    dropdown={
        'protocol': {
            'options': [{'label': i, 'value': i} for i in utils.get_options(subject.Subject.Protocol, 'protocol')]
        },
    })

## ------------------------- add subject protocols button -------------------------------
add_subject_protocols_button = html.Button(
    children='Add subject protocols',
    id='add-subject-protocols-button', n_clicks=0,
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

## ------------------------- filter of user ----------------------------------------
user_filter_dropdown = dcc.Dropdown(
    id='user-filter-dropdown',
    options=[
        {'label': user, 'value': user} for user in (dj.U('user') & subject.Subject.User) .fetch('user')
    ],
    style={'width': '200px', 'marginBottom': '0.5em'},
    placeholder='Select user ...',
)


## ------------------------- subject tab -------------------------------------
subject_tab = html.Div(
    [
        html.Div(
            [
                add_subject_button,
                add_subject_table,
            ],
            style={'marginBottom': '1em',
                   'display': 'inline-block'}
        ),
        html.Div(
            [
                add_subject_users_button,
                add_subject_users_table
            ],
            style={'display': 'inline-block'}
        ),
        html.Div(
            [
                add_subject_protocols_button,
                add_subject_protocols_table
            ],
            style={'display': 'inline-block'}
        ),
        html.Div(
            [
                'Subject User',
                user_filter_dropdown,
            ]
        ),
        html.Div(
            [
                delete_subject_button,
                update_subject_button
            ],
            style={'marginBottom': '0.5em'}),
        html.Div(
            [
                subject_table
            ],
            style={'marginBottom': '1em',
                   'display': 'inline-block'}),
        html.Div(
            [
                subject_users_table
            ],
            style={'marginBottom': '1em',
                   'display': 'inline-block'}
        ),
        html.Div(
            [
                subject_protocols_table
            ],
            style={'marginBottom': '1em',
                   'display': 'inline-block'}
        ),
    ])

## ========================= Construct webpage layout ========================
app.layout = html.Div([
    dcc.Tabs(id="tabs", value='Subject', children=[
        dcc.Tab(label='Lab', value='Lab'),
        dcc.Tab(label='Subject', value='Subject'),
        dcc.Tab(label='Surgery', value='Surgery'),
        dcc.Tab(label='Session', value='Session')
    ],
    style={'width': '30%', 'marginBottom': '2em'}),
    html.Div(id='tabs-content')
])


## ========================= Callback functions =========================

@app.callback(Output('tabs-content', 'children'),
              [Input('tabs', 'value')])
def render_content(tab):
    if tab == 'Subject':
        return subject_tab
    elif tab == 'Lab':
        return html.Div([
            html.H3('lab content')
        ])
    elif tab == 'Surgery':
        return html.Div([
            html.H3('Surgery content')
        ])
    elif tab == 'Session':
        return html.Div([
            html.H3('Session content')
        ])


@app.callback(
    # first argument is the id of a component, second is the field of that component
    Output('subject-table', 'data'), # function returns overwrite the 'data' here
    [Input('add-subject-button', 'n_clicks'),
     Input('delete-subject-button', 'n_clicks'),
     Input('update-subject-button', 'n_clicks'),
     Input('user-filter-dropdown', 'value')],
    [State('add-subject-table', 'data'),
     State('subject-table', 'data'),
     State('subject-table', 'selected_rows')])
# arguments of the call back function need to be the same order
# as the Input and State
def add_delete_subject(n_clicks_add, n_clicks_delete, n_clicks_update, user, new_data, data, selected_rows):
    ctx = dash.callback_context
    triggered_component = ctx.triggered[0]['prop_id'].split('.')[0]
    if triggered_component == 'add-subject-button':
        entry = {k: v for k, v in new_data[0].items() if v!=''}
        subject.Subject.insert1(entry)
        data = subject.Subject.fetch(as_dict=True)

    if triggered_component == 'delete-subject-button' and selected_rows:
        subj = {'subject_id': data[selected_rows[0]]['subject_id']}
        (subject.Subject & subj).delete()
        data = subject.Subject.fetch(as_dict=True)

    if triggered_component == 'user-filter-dropdown':
        if user:
            data = (subject.Subject & (subject.Subject.User & {'user': user})).fetch(
                as_dict=True)
        else:
            data = subject.Subject.fetch(as_dict=True)

    return data


@app.callback(
    [Output('delete-subject-button', 'disabled'),
     Output('update-subject-button', 'disabled'),
    ],
    [Input('subject-table', 'selected_rows'),
     State('subject-table', 'data')])
def update_selected_rows(selected_rows, data):
    if selected_rows:
        disabled = False
    else:
        disabled = True

    return disabled, disabled

@app.callback(
    [Output('subject-users-table', 'data'),
     Output('subject-protocols-table', 'data')],
    [Input('subject-table', 'selected_rows'),
     State('subject-table', 'data')]
)
def load_part_tables(selected_rows, data):
    if selected_rows:
        subj = {'subject_id': data[selected_rows[0]]['subject_id']}
        user_data = (subject.Subject.User & subj).fetch(as_dict=True)
        protocol_data = (subject.Subject.Protocol & subj).fetch(as_dict=True)
    else:
        user_data = [{c['id'] for c in subject_users_columns}]
        protocol_data = [{c['id'] for c in subject_protocols_columns}]
    return user_data, protocol_data

# @app.callback(
#     [],
#     [   Input('add-subject-users-button', 'n_clicks'),
#         State('add-subject-users-table', 'data')
#     ]
# )
# def insert_subject_users(n_clicks, data):

#     subject.Subject.User.insert(data)



## ========================= Run server =========================

if __name__ == '__main__':
    dj.config['safemode'] = False
    # run the server, debug = True allows auto-updating without restarting the server.
    app.run_server(debug=True)
