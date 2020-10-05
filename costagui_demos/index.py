
import datajoint as dj
import dash
import dash_table
from dash.dependencies import Input, Output, State
import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import copy
from dj_tables import lab, subject, hardware
import dj_utils
from costagui_demos.app import app

from tabs import subject_tab, hardware_tab

## ========================= Create a flask app ===========================
# dash does the job for you
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
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


## ========================= Run server =========================
if __name__ == '__main__':
    dj.config['safemode'] = False
    # run the server, debug = True allows auto-updating without restarting the server.
    app.run_server(debug=True)
