from dash.dependencies import Input, Output, State
import dash_html_components as html
import dash_core_components as dcc
from costagui_demos.app import app
from tabs import subject_tab_from_template, hardware_tab_from_template, surgery_tab_from_template
import datajoint as dj

dj.conn().close()

# ========================= Construct webpage layout ========================
tabs = html.Div(
    [
        dcc.Tabs(
            id="tabs", value='Subject',
            children=[
                dcc.Tab(id='lab-tab', label='Lab', value='Lab'),
                dcc.Tab(id='subject-tab', label='Subject', value='Subject'),
                dcc.Tab(id='surgery-tab', label='Surgery', value='Surgery'),
                dcc.Tab(id='session-tab', label='Session', value='Session'),
                dcc.Tab(id='hardware-tab', label='Hardware', value='Hardware')
            ],
            style={'width': '50%', 'marginBottom': '2em'}),
        html.Div(id='tabs-content')
    ]
)

log_in_page = html.Div(
    children=[
        html.H4('Welcome to the Costa Lab GUI'),
        html.H6('User name'),
        dcc.Input(
            id='user-name',
            type='text',
            placeholder=''
        ),
        html.H6('Password'),
        dcc.Input(
            id='password',
            type='password',
            placeholder='',
            style={'display': 'block', 'marginBottom': '1em'}
        ),
        html.Button(
            id='connection-button',
            children='Connect'
        ),
        html.H6(id='connection-status', children='Not connected')
    ],
    style={'marginTop': '3em', 'marginLeft': '5em'}
)

app.layout = html.Div(
    id='contents',
    children=log_in_page
)


# ========================= Callback functions =========================
@app.callback(Output('tabs-content', 'children'),
              [Input('tabs', 'value')])
def render_content(tab):

    if tab == 'Subject':
        return subject_tab_from_template.tab.layout
    elif tab == 'Lab':
        return html.Div([
            html.H3('lab content')
        ])
    elif tab == 'Surgery':
        return surgery_tab_from_template.surgery_table_tab.layout
    elif tab == 'Session':
        return html.Div([
            html.H3('Session content')
        ])
    elif tab == 'Hardware':
        return hardware_tab_from_template.table_layouts


@app.callback(
    [
        Output('contents', 'children'),
        Output('connection-status', 'children')
    ],
    [Input('connection-button', 'n_clicks')],
    [
        State('user-name', 'value'),
        State('password', 'value'),
        State('contents', 'children')
    ]
)
def render_page_contents(n_clicks, user, password, current_contents):

    if n_clicks:
        dj.config['database.host'] = '127.0.0.1'
        dj.config['database.user'] = user
        dj.config['database.password'] = password

        try:
            dj.conn().connect()
            return [tabs] + ['Connected']
        except Exception as e:
            return [current_contents] + [f'Connection failed: {str(e)}']
    else:
        return [current_contents] + ['Not connected']


# ========================= Run server =========================
if __name__ == '__main__':
    dj.config['safemode'] = False
    # run the server, debug = True allows auto-updating without restarting the server.
    app.run_server(debug=True)
