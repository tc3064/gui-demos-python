
import datajoint as dj
from dash.dependencies import Input, Output, State
import dash_html_components as html
import dash_core_components as dcc
from costagui_demos.app import app

# ========================= Construct webpage layout ========================
app.layout = html.Div(
    [
        dcc.Tabs(
            id="tabs", value='Log in',
            children=[
                dcc.Tab(id='log-in-tab', label='Log in', value='Log in'),
                dcc.Tab(id='lab-tab', label='Lab', value='Lab', disabled=True),
                dcc.Tab(id='subject-tab', label='Subject', value='Subject', disabled=True),
                dcc.Tab(id='surgery-tab', label='Surgery', value='Surgery', disabled=True),
                dcc.Tab(id='session-tab', label='Session', value='Session', disabled=True),
                dcc.Tab(id='hardware-tab', label='Hardware', value='Hardware', disabled=True)
            ],
            style={'width': '50%', 'marginBottom': '2em'}),
        html.Div(id='tabs-content')
    ]
)


# ========================= Callback functions =========================
@app.callback(Output('tabs-content', 'children'),
              [Input('tabs', 'value')])
def render_content(tab):

    if tab == 'Log in':
        from tabs import log_in_tab
        return log_in_tab.log_in_tab_contents
    elif tab == 'Subject':
        from tabs import subject_tab
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
    elif tab == 'Hardware':
        from tabs import hardware_tab_from_template
        return hardware_tab_from_template.hardware_tab_contents


tabs = ['lab-tab', 'subject-tab', 'surgery-tab', 'session-tab', 'hardware-tab']
@app.callback(
    [Output(tab, 'disabled') for tab in tabs] +
    [Output('connection-status', 'children')],
    [Input('connection-button', 'n_clicks')],
    [
        State('user-name', 'value'),
        State('password', 'value')
    ]
)
def enable_tabs(n_clicks, user, password):

    if n_clicks:
        dj.config['database.host'] = '127.0.0.1'
        dj.config['database.user'] = user
        dj.config['database.password'] = password

        try:
            dj.conn()
            return tuple([False for tab in tabs] + ['Connected.'])
        except Exception as e:
            return tuple([True for tab in tabs] + [
                f'Connection error: {str(e)}'])
    else:
        return tuple([True for tab in tabs] + ['Not Connected.'])


# ========================= Run server =========================
if __name__ == '__main__':
    dj.config['safemode'] = False
    # run the server, debug = True allows auto-updating without restarting the server.
    app.run_server(debug=True)
