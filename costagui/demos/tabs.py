import datajoint as dj
import dash
import dash_table
from dash.dependencies import Input, Output, State
import dash_html_components as html
import dash_core_components as dcc

from dj_tables import lab, subject


app = dash.Dash(__name__)

subjs = subject.Subject.fetch(as_dict=True)
columns = [{"name": i, "id": i} for i in subject.Subject.heading.names]

table_style_template = dict(
    fixed_columns={'headers': True, 'data': 1},
    style_cell={
        'textAlign': 'left',
        'fontSize':12,
        'font-family':'helvetica',
        'minWidth': '120px', 'width': '120px', 'maxWidth': '120px',
        'overflow': 'hidden',
        'height': '30px'},
    page_action='none',
    style_table={
        'minWidth': '1000px',
        'width': '1000px',
        'maxWidth': '1000px',
        'overflowY': 'scroll',
        'overflowX': 'scroll'},
    style_header={
        'backgroundColor': 'rgb(220, 220, 220)',
        'fontWeight': 'bold'})


subject_table = dash_table.DataTable(
    id='subject-table',
    columns=columns,
    data=subjs,
    # editable=True,
    # allow sorting
    sort_action='native',
    # allow filtering
    filter_action='native',
    # allow selecting a single entry
    row_selectable='single',
    **table_style_template
)

subject_tab = html.Div(
    [subject_table]
)


app.layout = html.Div([
    dcc.Tabs(id="tabs", value='Subject', children=[
        dcc.Tab(label='Lab', value='Lab'),
        dcc.Tab(label='Subject', value='Subject'),
        dcc.Tab(label='Surgery', value='Surgery'),
        dcc.Tab(label='Session', value='Session')
    ],
    style={'width': '60%', 'marginBottom': '2em'}),
    html.Div(id='tabs-content')
])


@app.callback(Output('tabs-content', 'children'),
              [Input('tabs', 'value')])
def render_content(tab):
    if tab == 'Subject':
        return subject_tab
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


if __name__ == '__main__':
    app.run_server(debug=True)
