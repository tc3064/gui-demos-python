import dash
import dash_table
from dash.dependencies import Input, Output, State
import dash_html_components as html
import dash_core_components as dcc

app = dash.Dash(__name__)

subject_id_input = dcc.Input(
    id='subject-id-input',
    type='text',
    placeholder='Input subject_id ...',
    value='mouse 1',
    style={
        'marginRight': '1em',
        'marginBottom': '2em'}
)

subject_nickname_input = dcc.Input(
    id='subject-nickname-input',
    type='text',
    placeholder='Input subject_nickname ...',
    value='mouse nickname',
    style={
        'marginRight': '1em',
        'marginBottom': '2em'}
)

display_subject_id_button = html.Button(
    id='display-subject-id-button',
    children='Display subject ID',
    n_clicks=0,
    style = {
        'display': 'block',
        'marginBottom': '2em'}
)

display_subject_nickname_button = html.Button(
    id='display-subject-nickname-button',
    children='Display subject nickname',
    n_clicks=0,
    style = {
        'marginBottom': '2em'}
)

display_subject_id_text = dcc.Textarea(
    id='display-subject-id-text',
    value='Subject id is:\n',
    style={
        'display': 'block'
    }
)


app.layout = html.Div(
    [
        subject_id_input,
        subject_nickname_input,
        display_subject_id_button,
        display_subject_nickname_button,
        display_subject_id_text,
    ]
)

@app.callback(
    # first argument is the id of a component, second is the field of that component
    Output('display-subject-id-text', 'value'), # function returns overwrite the 'data' here
    [Input('display-subject-id-button', 'n_clicks'),
     Input('display-subject-nickname-button', 'n_clicks'),
     State('subject-id-input', 'value'),
     State('subject-nickname-input', 'value')])
def display_subject_id(n_clicks_id, n_clicks_nickname, id_value, nickname_value):

    ctx = dash.callback_context
    triggered_component = ctx.triggered[0]['prop_id'].split('.')[0]

    if triggered_component == 'display-subject-id-button':
        return 'Subject id is:\n {}'.format(id_value)

    elif triggered_component == 'display-subject-nickname-button':
        return 'Subject nickname is:\n {}'.format(nickname_value)


if __name__ == '__main__':

    app.run_server(debug=True)
