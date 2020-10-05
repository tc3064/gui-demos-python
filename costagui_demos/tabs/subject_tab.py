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
    subject.Subject, 'subject-table', height='800px')

add_subject_table = component_utils.create_add_record_table(
    subject.Subject, 'add-subject-table',
    dropdown_fields=['sex', 'subject_strain'], height='200px')

# add subject button
add_subject_button = html.Button(
    children='Add a subject record',
    id='add-subject-button', n_clicks=0,
    style={'marginBottom': '0.5em'})

# deletion confirm dialogue
delete_subject_confirm = dcc.ConfirmDialog(
    id='delete-subject-confirm',
    message='Are you sure you want to delete the record?',
),

delete_subject_button = html.Button(
    children='Delete the current record',
    id='delete-subject-button', n_clicks=0,
    style={'marginRight': '1em'})

update_subject_button = html.Button(
    children='Update the current record',
    id='update-subject-button', n_clicks=0,
)

# -------- Pop up window with update table and message ------
update_subject_modal = component_utils.create_update_modal(
    subject.Subject, 'subject',
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

# form subject tab
subject_tab_contents = html.Div(
    html.Div(
        className="row app-body",
        children=[
            html.Div(
                [add_subject_button, add_subject_table],
                style={'marginBottom': '3em'}
            ),

            html.Div(
                [
                    html.Div(
                        [
                            delete_subject_button,
                            update_subject_button
                        ],
                        style={'marginBottom': '0.5em'}),
                    user_filter_dropdown,
                    html.Div(
                        [subject_table],
                        style={'marginBottom': '1em'}),
                ]
            )
        ]

    )
)


# ------------------------- subject callback --------------------------------
@app.callback(
    # first argument is the id of a component, second is the field of that component
    Output('subject-table', 'data'),  # function returns overwrite the 'data' here
    [Input('add-subject-button', 'n_clicks'),
     Input('delete-subject-button', 'n_clicks'),
     Input('update-subject-button', 'n_clicks'),
     Input('user-filter-dropdown', 'value')],
    [State('add-subject-table', 'data'),
     State('subject-table', 'data'),
     State('subject-table', 'selected_rows')])
# arguments of the call back function need to be the same order
# as the Input and State
def update_subject_data(n_clicks_add, n_clicks_delete, n_clicks_update,
                        user, new_data, data, selected_rows):
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
     Output('update-subject-button', 'disabled')],
    [Input('subject-table', 'selected_rows')])
def set_button_enabled_state(selected_rows):
    if selected_rows:
        disabled = False
    else:
        disabled = True
    return disabled, disabled


@app.callback(
    [Output('update-subject-modal', 'is_open'),
     Output('update-subject-table', 'data')],
    [Input('update-subject-button', 'n_clicks'), Input('close', 'n_clicks')],
    [State('update-subject-modal', 'is_open'),
     State('subject-table', 'data'),
     State('subject-table', 'selected_rows')],
)
def toggle_modal(n1, n2, is_open, data, selected_rows):
    if n1 or n2:
        return not is_open, [data[selected_rows[0]]]

    return is_open, [data[selected_rows[0]]]


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
        if new[f] != old[f] and not (old is None and new==''):
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
    app.layout = html.Div(
        [
            subject_tab_contents,
            update_subject_modal,
        ]
    )

    app.run_server(debug=True)
