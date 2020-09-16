import dash
import dash_table
import dash_html_components as html
import dash_core_components as dcc

from dj_tables import lab, subject

app = dash.Dash()

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
    editable=True,
    # allow sorting
    sort_action='native',
    # allow filtering
    filter_action='native',
    # allow selecting a single entry
    row_selectable='single',
    **table_style_template
)

app.layout = html.Div(
    children=[
        'Mouse table',
        subject_table
])

# If I run this module as a script
if __name__ == '__main__':
    app.run_server(debug=True)
