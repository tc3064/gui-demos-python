import datajoint as dj
from costagui_demos.app import app
import dash_html_components as html
import dash_core_components as dcc


log_in_tab_contents = html.Div(
    children=[
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

if __name__ == '__main__':
    dj.config['safemode'] = False
    app.layout = log_in_tab_contents
    app.run_server(debug=True)
