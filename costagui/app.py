# %%
import datajoint as dj
import dash
import dash_table
from dash.dependencies import Input, Output, State
import dash_html_components as html
import dash_core_components as dcc
import copy
# %%
from dj_tables import lab, subject
import utils

import subject_tab, hardware_tab

## ========================= Create a flask app ===========================
# dash does the job for you
app = dash.Dash(__name__)
app.config.suppress_callback_exceptions = True

## ========================= Construct webpage layout ========================
app.layout = html.Div([
    dcc.Tabs(id="tabs", value='Subject', children=[
        dcc.Tab(label='Lab', value='Lab'),
        dcc.Tab(label='Subject', value='Subject'),
        dcc.Tab(label='Surgery', value='Surgery'),
        dcc.Tab(label='Session', value='Session'),
        dcc.Tab(label='Hardware', value='Hardware')
    ],
    style={'width': '50%', 'marginBottom': '2em'}),
    html.Div(id='tabs-content')
])

## ========================= Callback functions =========================
@app.callback(Output('tabs-content', 'children'),
              [Input('tabs', 'value')])
def render_content(tab):
    if tab == 'Subject':
        return subject_tab.subject_tab_contents
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
    elif tab =='Hardware':
        return hardware_tab.hardware_tab_contents


## ------------------------- subject callback --------------------------------
@app.callback(
    # first argument is the id of a component, second is the field of that component
    Output('subject-table', 'data'), # function returns overwrite the 'data' here
    [Input('add-subject-button', 'n_clicks'),
     Input('delete-subject-button', 'n_clicks')],
    [State('add-subject-table', 'data'),
     State('subject-table', 'data'),
     State('subject-table', 'selected_rows')])
# arguments of the call back function need to be the same order
# as the Input and State
def add_subject(n_clicks_add, n_clicks_delete, new_data, data, selected_rows):
    ctx = dash.callback_context
    triggered_component = ctx.triggered[0]['prop_id'].split('.')[0]
    if triggered_component == 'add-subject-button':
        entry = {k: v for k, v in new_data[0].items() if v!=''}
        subject.Subject.insert1(entry)
        data = subject.Subject.fetch(as_dict=True)

    if triggered_component == 'delete-subject-button' and selected_rows:
        print(selected_rows)
        subj = {'subject_id': data[selected_rows[0]]['subject_id']}
        (subject.Subject & subj).delete()
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

## ------------------------- hardware callback --------------------------------

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
        print('trying to delete row: {}'.format(selected_rows))
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


## ========================= Run server =========================
if __name__ == '__main__':
    dj.config['safemode'] = False
    # run the server, debug = True allows auto-updating without restarting the server.
    app.run_server(debug=True)
