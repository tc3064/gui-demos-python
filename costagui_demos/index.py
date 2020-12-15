
import datajoint as dj
from dash.dependencies import Input, Output
import dash_html_components as html
import dash_core_components as dcc
from costagui_demos.app import app

from tabs import subject_tab, hardware_tab_from_template

# ========================= Construct webpage layout ========================
app.layout = html.Div(
    [
        dcc.Tabs(
            id="tabs", value='Subject',
            children=[
                dcc.Tab(label='Lab', value='Lab'),
                dcc.Tab(label='Subject', value='Subject'),
                dcc.Tab(label='Surgery', value='Surgery'),
                dcc.Tab(label='Session', value='Session'),
                dcc.Tab(label='Hardware', value='Hardware')
            ],
            style={'width': '50%', 'marginBottom': '2em'}),
        html.Div(id='tabs-content')
    ]
)


# ========================= Callback functions =========================
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
    elif tab == 'Hardware':
        return hardware_tab_from_template.hardware_tab_contents


# ========================= Run server =========================
if __name__ == '__main__':
    dj.config['safemode'] = False
    # run the server, debug = True allows auto-updating without restarting the server.
    app.run_server(debug=True)
