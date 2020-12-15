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
            # modals
            update_subject_modal,
            add_subject_modal,
            # state variables
            subject_user_state
        ]

    )
)


if __name__ == '__main__':
    dj.config['safemode'] = False
    app.layout = subject_tab_contents
    app.run_server(debug=True)
