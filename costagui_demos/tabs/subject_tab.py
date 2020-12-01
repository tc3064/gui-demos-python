import datajoint as dj
import dash
import dash_table
from dash.dependencies import Input, Output, State
import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc
from costagui_demos.app import app
from costagui_demos.dj_tables import lab, subject, hardware
from costagui_demos import dj_utils, component_utils, callback_utils
import datetime


# relative variables for subject tables
subject_primary_key = subject.Subject.heading.primary_key
subject_field_names = subject.Subject.heading.names
subject_user_field_names = subject.Subject.User.heading.names
subject_protocol_field_names = subject.Subject.Protocol.heading.names


subject_table = component_utils.create_display_table(
    subject.Subject, 'subject-table', height='800px', width='800px')


button_style = {
    'marginRight': '1em',
    'marginBottom': '1em'}

# add subject button
add_subject_button = html.Button(
    children='Add a subject record',
    id='add-subject-button', n_clicks=0,
    style=button_style)

add_subject_modal = component_utils.create_modal(
    subject.Subject, 'subject', include_parts=True,
    dropdown_fields=['sex', 'subject_strain'],
    mode='add'
)

# deletion confirm dialogue
delete_subject_confirm = dcc.ConfirmDialog(
    id='delete-subject-confirm',
    message='Are you sure to delete the record?',
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
update_subject_modal = component_utils.create_modal(
    subject.Subject, 'subject', include_parts=True,
    dropdown_fields=['sex', 'subject_strain'],
    mode='update'
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
subject_user_table = component_utils.create_display_table(
    subject.Subject.User, 'subject-user-table',
    excluded_fields=['subject_id'], empty_first=True,
    height='200px', width='110px', selectable=False)


# -------- part table subject.Subject.Protocol ---------------
subject_protocol_table = component_utils.create_display_table(
    subject.Subject.Protocol, 'subject-protocol-table',
    excluded_fields=['subject_id'], empty_first=True,
    height='200px', width='260px', selectable=False)


# ----------------------- Message boxes ----------------------------------
messagebox_style = {
    'width': 750,
    'height': 50,
    'marginBottom': '1em',
    'display': 'block'}

delete_subject_message_box = dcc.Textarea(
    id='delete-subject-message-box',
    value='Delete subject message:',
    style=messagebox_style
)


# ---------------- state variables -------------------

subject_user_state = html.Div(
    id='subject-user-state',
    children=[])


# construct subject tab
subject_tab_contents = html.Div(
    html.Div(
        className="row app-body",
        children=[
            html.Div(
                [
                    html.Div(
                        [
                            html.Div(
                                [
                                    html.Div(
                                        add_subject_button,
                                        style={'display': 'inline-block'}),
                                    html.Div(
                                        delete_subject_button,
                                        style={'display': 'inline-block'}),
                                    html.Div(
                                        update_subject_button,
                                        style={'display': 'inline-block'})
                                ],
                            ),
                            delete_subject_message_box,
                        ]
                    ),
                    user_filter_dropdown,
                    html.Div(
                        [
                            html.H6('Subject'),
                            subject_table
                        ],
                        style={'marginRight': '1em',
                               'display': 'inline-block'}),
                    html.Div(
                        [
                            html.H6('Subject.User'),
                            subject_user_table
                        ],
                        style={'marginRight': '1em',
                               'display': 'inline-block'}
                    ),
                    html.Div(
                        [
                            html.H6('Subject.Protocol'),
                            subject_protocol_table
                        ],
                        style={'marginRight': '1em',
                               'display': 'inline-block'}
                    ),
                ]
            ),
            # confirmation dialogue
            html.Div(delete_subject_confirm),
            # modals
            update_subject_modal,
            add_subject_modal,
            # state variables
            subject_user_state,
        ]

    )
)


# ------------------------- subject callback --------------------------------

# callback for user state variable
@app.callback(
    Output('subject-user-state', 'children'),
    [Input('user-filter-dropdown', 'value')]
)
def update_user_state(user):
    return user


@app.callback(
    Output('delete-subject-confirm', 'displayed'),
    [Input('delete-subject-button', 'n_clicks')])
def display_confirm(n_clicks):
    if n_clicks:
        return True
    return False


# callback to update subject table data

@app.callback(
    # Output fields to update
    # first argument is the id of a component,
    # second is the field of that component
    [Output('subject-table', 'data'),
     Output('subject-user-table', 'data'),
     Output('subject-protocol-table', 'data'),
     Output('delete-subject-message-box', 'value')],
    # Input fields that the callback functions responds to
    [
        Input('add-subject-close', 'n_clicks'),
        Input('delete-subject-confirm', 'submit_n_clicks'),
        Input('update-subject-close', 'n_clicks'),
        Input('subject-user-state', 'children'),
        Input('subject-table', 'selected_rows')
    ],
    # State variables that the callback function uses, but does not
    # respond to whose changes
    [
        State('subject-table', 'data'),
    ]
)
# arguments of the call back function need to be the same order
# as the Input and State
def update_subject_table_data(
        n_clicks_add_close, n_clicks_delete, n_clicks_update_close,
        user, selected_rows, data):

    delete_message = 'Delete subject message:\n'
    ctx = dash.callback_context
    triggered_component = ctx.triggered[0]['prop_id'].split('.')[0]

    if triggered_component == 'delete-subject-confirm' and selected_rows:
        subj = {'subject_id': data[selected_rows[0]]['subject_id']}
        try:
            (subject.Subject & subj).delete()
            delete_message = delete_message + \
                f'Successfully deleted record {subj}!'
        except Exception as e:
            delete_message = delete_message + \
                f'Error in deleting record {subj}: {str(e)}.'

    if user:
        data = (subject.Subject & (subject.Subject.User & {'user': user})).fetch(
            as_dict=True)
    else:
        data = subject.Subject.fetch(as_dict=True)

    if selected_rows:
        subj = {'subject_id': data[selected_rows[0]]['subject_id']}
        user_data = (subject.Subject.User & subj).fetch(as_dict=True)
        protocol_data = (subject.Subject.Protocol & subj).fetch(as_dict=True)
    else:
        user_data = [
            {f: '' for f in subject_user_field_names}]
        protocol_data = [
            {f: '' for f in subject_protocol_field_names}]

    return data, user_data, protocol_data, delete_message


@app.callback(
    [
        Output('add-subject-modal', 'is_open'),
        Output('add-subject-table', 'data'),
        Output('add-subject-user-table', 'data'),
        Output('add-subject-protocol-table', 'data')
    ],
    [
        Input('add-subject-button', 'n_clicks'),
        Input('add-subject-close', 'n_clicks'),
        Input('add-subject-user-add-row-button', 'n_clicks'),
        Input('add-subject-protocol-add-row-button', 'n_clicks')
    ],
    [
        State('add-subject-modal', 'is_open'),
        State('subject-table', 'data'),
        State('subject-table', 'selected_rows'),
        State('subject-user-table', 'data'),
        State('subject-protocol-table', 'data'),
        State('add-subject-table', 'data'),
        State('add-subject-user-table', 'data'),
        State('add-subject-protocol-table', 'data'),
    ],
)
def toggle_add_modal(
        n_open, n_close,
        n_add_user_row, n_add_protocol_row,
        is_open, subject_data, selected_rows,
        subject_user_data, subject_protocol_data,
        add_subject_data,
        add_subject_user_data, add_subject_protocol_data):

    ctx = dash.callback_context
    triggered_component = ctx.triggered[0]['prop_id'].split('.')[0]

    if triggered_component == 'add-subject-button':
        if selected_rows:
            add_subject_data = [subject_data[selected_rows[0]]]
            add_subject_user_data = subject_user_data
            add_subject_protocol_data = subject_protocol_data
        else:
            add_subject_data = [{k: '' for k in subject_field_names}]
            add_subject_user_data = [
                {k: '' for k in subject_user_field_names
                 if k not in subject_primary_key}]
            add_subject_protocol_data = [
                {k: '' for k in subject_protocol_field_names
                 if k not in subject_primary_key}]
        add_modal_open = not is_open if n_open or n_close else is_open

    elif triggered_component == 'add-subject-user-add-row-button':
        add_subject_user_data = add_subject_user_data + \
            [
                {k: '' for k in subject_user_field_names
                 if k not in subject_primary_key}
            ]
        add_modal_open = is_open

    elif triggered_component == 'add-subject-protocol-add-row-button':
        add_subject_protocol_data = add_subject_protocol_data + \
            [
                {k: '' for k in subject_protocol_field_names
                 if k not in subject_primary_key}
            ]
        add_modal_open = is_open

    elif triggered_component == 'add-subject-close':
        add_modal_open = not is_open if n_open or n_close else is_open

    else:
        add_modal_open = is_open

    return add_modal_open, add_subject_data, add_subject_user_data, \
        add_subject_protocol_data


@app.callback(
    Output('add-subject-message', 'value'),
    [
        Input('add-subject-confirm', 'n_clicks'),
        Input('add-subject-close', 'n_clicks')
    ],
    [
        State('add-subject-table', 'data'),
        State('add-subject-user-table', 'data'),
        State('add-subject-protocol-table', 'data'),
        State('add-subject-message', 'value')
    ]
)
def add_subject_record(
        n_clicks_add, n_clicks_close,
        new_subject_data, new_users_data, new_protocols_data,
        add_subject_message):

    ctx = dash.callback_context
    triggered_component = ctx.triggered[0]['prop_id'].split('.')[0]

    if triggered_component == 'add-subject-confirm':
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
        add_subject_message = 'Add message:'
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

    elif triggered_component == 'add-subject-close':
        add_subject_message = 'Add message:'

    return add_subject_message


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
        Output('update-subject-user-table', 'data'),
        Output('update-subject-protocol-table', 'data')
    ],
    [
        Input('update-subject-button', 'n_clicks'),
        Input('update-subject-close', 'n_clicks'),
        Input('update-subject-user-add-row-button', 'n_clicks'),
        Input('update-subject-protocol-add-row-button', 'n_clicks')
    ],
    [
        State('update-subject-modal', 'is_open'),
        State('subject-table', 'data'),
        State('subject-table', 'selected_rows'),
        State('subject-user-table', 'data'),
        State('subject-protocol-table', 'data'),
        State('update-subject-user-table', 'data'),
        State('update-subject-protocol-table', 'data'),
    ],
)
def toggle_update_modal(
        n_open, n_close, n_add_user_row, n_add_protocol_row,
        is_open,
        subject_data, selected_rows,
        subject_user_data, subject_protocol_data,
        update_subject_user_data, update_subject_protocol_data
        ):

    ctx = dash.callback_context
    triggered_component = ctx.triggered[0]['prop_id'].split('.')[0]

    if triggered_component == 'update-subject-user-add-row-button':
        update_subject_user_data = update_subject_user_data + \
            [
                {k: ('' if k not in subject_primary_key
                     else subject_data[selected_rows[0]][k])
                 for k in subject_user_field_names}
            ]
        update_modal_open = is_open

    elif triggered_component == 'update-subject-protocol-add-row-button':
        update_subject_protocol_data = update_subject_protocol_data + \
            [
                {k: ('' if k not in subject_primary_key
                     else subject_data[selected_rows[0]][k])
                 for k in subject_protocol_field_names}
            ]
        update_modal_open = is_open

    elif triggered_component == 'update-subject-button':
        if not selected_rows:
            raise ValueError('Update Modal open without a particular row selected')

        update_subject_user_data = subject_user_data
        update_subject_protocol_data = subject_protocol_data

        update_modal_open = not is_open if n_open or n_close else is_open

    else:
        update_subject_user_data = [
            {k: '' for k in subject_user_field_names}
        ]
        update_subject_protocol_data = [
            {k: '' for k in subject_protocol_field_names}
        ]
        update_modal_open = not is_open if n_open or n_close else is_open

    if selected_rows:
        update_subject_data = [subject_data[selected_rows[0]]]
    else:
        update_subject_data = [
            {k: '' for k in subject_field_names}
        ]

    return update_modal_open, update_subject_data, \
        update_subject_user_data, update_subject_protocol_data


subject_fields = subject.Subject.heading.secondary_attributes


@app.callback(
    Output('update-subject-message', 'value'),
    [
        Input('update-subject-confirm', 'n_clicks')
    ],
    [
        State('update-subject-table', 'data'),
        State('update-subject-user-table', 'data'),
        State('update-subject-protocol-table', 'data')
    ],
)
def update_subject_record(
        n_clicks, update_subject_data,
        update_subject_user_data, update_subject_protocol_data):

    new = update_subject_data[0]
    if not new['subject_id']:
        return 'Update message:'

    subj_key = {'subject_id': new['subject_id']}
    old = (subject.Subject & subj_key).fetch1()

    msg = 'Update message:\n'
    for f in table.heading.secondary_attributes:
        if new[f] != old[f] and not (old is None and new == ''):
            try:
                dj.Table._update(table & pk, f, new[f])
                msg = msg + f'Successfully updated field {f} ' + \
                    f'from {old[f]} to {new[f]}!\n'
            except Exception as e:
                msg = msg + str(e) + '\n'

    msg = callback_utils.update_part_table(
        subject.Subject.User, subj_key, update_subject_user_data, msg)

    msg = callback_utils.update_part_table(
        subject.Subject.Protocol, subj_key, update_subject_protocol_data, msg)

    return msg


if __name__ == '__main__':
    dj.config['safemode'] = False
    app.layout = subject_tab_contents
    app.run_server(debug=True)
