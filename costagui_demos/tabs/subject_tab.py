import datajoint as dj
import dash
import dash_table
from dash.dependencies import Input, Output, State
import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc
from costagui_demos.app import app
from costagui_demos.dj_tables import lab, subject, hardware
from costagui_demos import dj_utils, component_utils
import datetime


subject_table = component_utils.create_display_table(
    subject.Subject, 'subject-table', height='800px', width='800px')

add_subject_table = component_utils.create_add_record_table(
    subject.Subject, 'add-subject-table',
    dropdown_fields=['sex', 'subject_strain'], height='200px', width='800px')


button_style = {
    'marginRight': '1em',
    'marginBottom': '1em'}

# add subject button
add_subject_button = html.Button(
    children='Add a subject record',
    id='add-subject-button', n_clicks=0,
    style=button_style)

# deletion confirm dialogue
delete_subject_confirm = dcc.ConfirmDialog(
    id='delete-subject-confirm',
    message='Are you sure you want to delete the record?',
),

delete_subject_button = html.Button(
    children='Delete the current record',
    id='delete-subject-button', n_clicks=0,
    style=button_style
)

update_subject_button = html.Button(
    children='Update the current record',
    id='update-subject-button', n_clicks=0,
    style=button_style
)

# -------- Pop up window with update table and message ------
update_subject_modal = component_utils.create_update_modal(
    subject.Subject, 'subject', include_parts=True,
    dropdown_fields=['sex', 'subject_strain']
)

user_filter_dropdown = dcc.Dropdown(
    id='user-filter-dropdown',
    options=[
        {'label': user, 'value': user}
        for user in (dj.U('user') & subject.Subject.User).fetch('user')
    ],
    style={'width': '200px', 'marginBottom': '0.5em'},
    placeholder='Select user ...',
)

# -------- part table subject.Subject.User -------------------
subject_users_table = component_utils.create_display_table(
    subject.Subject.User, 'subject-users-table',
    excluded_fields=['subject_id'], empty_first=True,
    height='200px', width='110px', selectable=False)

add_subject_users_table = component_utils.create_add_record_table(
    subject.Subject.User, 'add-subject-users-table', n_rows=3,
    dropdown_fields=['user'], excluded_fields=['subject_id'],
    height='200px', width='110px')

add_subject_users_button = html.Button(
    children='Add subject users',
    id='add-subject-users-button', n_clicks=0,
    style=button_style)


# -------- part table subject.Subject.Protocol ---------------
subject_protocols_table = component_utils.create_display_table(
    subject.Subject.Protocol, 'subject-protocols-table',
    excluded_fields=['subject_id'], empty_first=True,
    height='200px', width='260px', selectable=False)

add_subject_protocols_table = component_utils.create_add_record_table(
    subject.Subject.Protocol, 'add-subject-protocols-table', n_rows=3,
    dropdown_fields=['subject_protocol'], excluded_fields=['subject_id'],
    height='200px', width='260px')

add_subject_protocols_button = html.Button(
    children='Add subject protocols',
    id='add-subject-protocols-button', n_clicks=0,
    style=button_style)


# ----------------------- Message boxes ----------------------------------
messagebox_style = {
    'width': 750,
    'height': 50,
    'marginBottom': '1em',
    'display': 'block'}

add_subject_message_box = dcc.Textarea(
    id='add-subject-message-box',
    value='Add subject message:',
    style=messagebox_style
)

delete_subject_message_box = dcc.Textarea(
    id='delete-subject-message-box',
    value='Delete subject message:',
    style=messagebox_style
)


# form subject tab
subject_tab_contents = html.Div(
    html.Div(
        className="row app-body",
        children=[
            html.Div(
                [
                    html.Div(
                        add_subject_button,
                        style={'display': 'block'}
                    ),
                    add_subject_message_box,
                    html.Div(
                        [
                            html.H6('Subject'),
                            add_subject_table
                        ],
                        style={'marginRight': '1em',
                               'display': 'inline-block'}
                    ),
                    html.Div(
                        [
                            html.H6('Subject.User'),
                            add_subject_users_table
                        ],
                        style={'marginRight': '1em',
                               'display': 'inline-block'}
                    ),
                    html.Div(
                        [
                            html.H6('Subject.Protocol'),
                            add_subject_protocols_table
                        ],
                        style={'marginRight': '1em',
                               'display': 'inline-block'}
                    )
                ],
                style={'marginBottom': '3em'}
            ),

            html.Div(
                [
                    html.Div(
                        [
                            html.Div(
                                [
                                    html.Div(delete_subject_button,
                                             style={'display': 'inline-block'}),
                                    html.Div(update_subject_button,
                                             style={'display': 'inline-block'})
                                ],
                            ),
                            delete_subject_message_box,
                        ]
                    ),
                    user_filter_dropdown,
                    html.Div(
                        [
                            subject_table
                        ],
                        style={'marginRight': '1em',
                               'display': 'inline-block'}),
                    html.Div(
                        [
                            subject_users_table
                        ],
                        style={'marginRight': '1em',
                               'display': 'inline-block'}
                    ),
                    html.Div(
                        [
                            subject_protocols_table
                        ],
                        style={'marginRight': '1em',
                               'display': 'inline-block'}
                    ),
                ]
            ),
            update_subject_modal
        ]

    )
)


# ------------------------- subject callback --------------------------------
@app.callback(
    # Output fields to update
    [
        # first argument is the id of a component,
        # second is the field of that component
        Output('subject-table', 'data'),
        Output('add-subject-message-box', 'value')
    ],
    # Input fields that the callback functions responds to
    [
        Input('add-subject-button', 'n_clicks'),
        Input('delete-subject-button', 'n_clicks'),
        Input('update-subject-button', 'n_clicks'),
        Input('user-filter-dropdown', 'value')
    ],
    # State variables that the callback function uses, but does not
    # respond to whose changes
    [
        State('add-subject-table', 'data'),
        State('add-subject-users-table', 'data'),
        State('add-subject-protocols-table', 'data'),
        State('subject-table', 'data'),
        State('subject-table', 'selected_rows'),
        State('add-subject-message-box', 'value')
    ]
)
# arguments of the call back function need to be the same order
# as the Input and State
def update_subject_table_data(
        n_clicks_add, n_clicks_delete, n_clicks_update,
        user, new_subject_data, new_users_data, new_protocols_data,
        data, selected_rows, add_subject_message):
    ctx = dash.callback_context
    triggered_component = ctx.triggered[0]['prop_id'].split('.')[0]

    if triggered_component == 'add-subject-button':

        # insert subject main table
        entry = {k: v for k, v in new_subject_data[0].items() if v != ''}
        users = [
            {**user, 'subject_id': new_subject_data[0]['subject_id']}
            for user in new_users_data if user['user']
        ]

        protocols = [
            {**protocol, 'subject_id': new_subject_data[0]['subject_id']}
            for protocol in new_protocols_data if protocol['protocol_assign_date']
        ]

        try:
            if (subject.Subject & {'subject_id': entry['subject_id']}):
                add_subject_message = add_subject_message + \
                    '\nWarning: subject {} exists in database'.format(entry['subject_id'])
            else:
                subject.Subject.insert1(entry)
                add_subject_message = add_subject_message + \
                    '\nSuccessful insertion to subject.Subject.'

        except Exception as e:
            add_subject_message = add_subject_message + \
                '\nError inserting into subject.Subject: {}'.format(str(e))

        try:
            subject.Subject.User.insert(users, skip_duplicates=True)
        except Exception as e:
            add_subject_message = add_subject_message + \
                '\nError inserting into subject.Subject.User: {}'.format(str(e))

        try:
            subject.Subject.Protocol.insert(protocols, skip_duplicates=True)
        except Exception as e:
            add_subject_message = add_subject_message + \
                '\nError inserting into subject.Subject.Protocol:{}'.format(str(e))

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

    return data, add_subject_message


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


@app.callback(
    [Output('delete-subject-button', 'disabled'),
     Output('update-subject-button', 'disabled')],
    [Input('subject-table', 'selected_rows')])
def set_button_enabled_state(selected_rows):
    if selected_rows:
        disabled = False
    else:
        disabled = True
    return disabled, disabled


@app.callback(
    [
        Output('update-subject-modal', 'is_open'),
        Output('update-subject-table', 'data'),
        Output('update-user-table', 'data'),
        Output('update-protocol-table', 'data')
    ],
    [
        Input('update-subject-button', 'n_clicks'),
        Input('close', 'n_clicks')
    ],
    [
        State('update-subject-modal', 'is_open'),
        State('subject-table', 'data'),
        State('subject-users-table', 'data'),
        State('subject-protocols-table', 'data'),
        State('subject-table', 'selected_rows'),
    ],
)
def toggle_modal(n1, n2, is_open,
                 subject_data, subject_users_data, subject_protocols_data,
                 selected_rows):

    if n1 or n2:
        return not is_open, [subject_data[selected_rows[0]]], \
            subject_users_data, subject_protocols_data

    return is_open, [data[selected_rows[0]]], \
        subject_users_data, subject_protocols_data


subject_fields = subject.Subject.heading.secondary_attributes


@app.callback(
    Output('update-subject-message', 'value'),
    [Input('update-subject-confirm', 'n_clicks')],
    [State('update-subject-table', 'data')],
)
def update_subject_record(n_clicks, data):
    new = data[0]
    subj_key = {'subject_id': new['subject_id']}
    old = (subject.Subject & subj_key).fetch1()

    msg = 'Update message:\n'
    for f in subject_fields:
        if new[f] != old[f] and not (old is None and new == ''):
            if type(old[f]) == datetime.date and \
                    old[f] == datetime.datetime.strptime(
                        new[f], '%Y-%m-%d').date():
                continue
            elif type(old[f]) == datetime.datetime and \
                    old[f] == datetime.datetime.strptime(
                        new[f], '%Y-%m-%dT%H:%M:%S'):
                continue

            try:
                dj.Table._update(subject.Subject & subj_key, f, new[f])
                msg = msg + f'Successfully updated field {f} from {old[f]} to {new[f]}!\n'
            except Exception as e:
                msg = msg + str(e) + '\n'
    return msg


if __name__ == '__main__':
    dj.config['safemode'] = False
    app.layout = subject_tab_contents
    app.run_server(debug=True)
