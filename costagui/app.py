import dash
import dash_table
from dash.dependencies import Input, Output, State
import dash_html_components as html
import copy

from dj_tables import lab, subject

# create a flask app (dash does the job for you)
app = dash.Dash(__name__)

# table style settings
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

# subject table style
subject_table_style = copy.deepcopy(table_style_template)
subject_table_style.update(
    style_data_conditional=[
        {'if': {'row_index': 'odd'},
        'backgroundColor': 'rgb(245, 245, 245)'}
    ],
    # allow sorting
    sort_action='native',
    # allow filtering
    filter_action='native',
    # allow selecting a single entry
    row_selectable='single')

subject_table_style['style_table'].update({
    'minHeight': '600px',
    'height': '600px',
    'maxHeight': '600px',
})

# add subject table
add_subject_style = copy.deepcopy(table_style_template)
add_subject_style['style_table'].update({
    'minHeight': '200px',
    'height': '200px',
    'maxHeight': '200px',
})

# from datajoint tables, get the data and table definition
subjs = subject.Subject.fetch(as_dict=True)
columns = [{"name": i, "id": i} for i in subject.Subject.heading.names]

# some fields are presented as dropdown list
for c in columns:
    if c['name'] == 'sex':
        c.update(presentation="dropdown")

# major page construction
app.layout = html.Div([
    html.Div([
        html.Button(children='Add a subject record', id='add-subject-button', n_clicks=0),
        dash_table.DataTable(
            id='add-subject-table',
            columns=columns,
            data=[{c['id']: '' for c in columns}],
            **add_subject_style,
            editable=True,
            dropdown={
                'sex': {
                    'options': [{'label': i, 'value': i} for i in [ 'M', 'F', 'U']]}
            },
        )], style={'marginBottom': '1em'}),

    html.Div([
        dash_table.DataTable(
            id='subject-table',
            columns=columns,
            data=subjs,
            # below are all styles
            **subject_table_style
            )],
        style={'marginBottom': '1em'})])


@app.callback(
    # first argument is the id of a component, second is the field of that component
    Output('subject-table', 'data'), # function returns overwrite the 'data' here
    [Input('add-subject-button', 'n_clicks')],
    [State('add-subject-table', 'data'),
     State('subject-table', 'data')])
# arguments of the call back function need to be the same order
# as the Input and State
def add_subject(n_clicks, new_data, data):
    if n_clicks > 0:
        entry = {k: v for k, v in new_data[0].items() if v!=''}
        subject.Subject.insert1(entry)
        data = subject.Subject.fetch(as_dict=True)
    return data


if __name__ == '__main__':
    # run the server, debug = True allows auto-updating without restarting the server.
    app.run_server(debug=True)
