import dash
import dash_table
import dash_html_components as html
import dash_core_components as dcc
import datetime

import dash_bootstrap_components as dbc

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

height = '40px'

subject_id_input = dcc.Input(
    id='subject-id-input',
    type='text',
    placeholder='Input subject_id ...',
    style={
        'marginRight': '1em',
        'marginBottom': '2em',
        'height': height}
)

subject_nickname_input = dcc.Input(
    id='subject-nickname-input',
    type='text',
    placeholder='Input subject_nickname ...',
    style={
        'marginRight': '1em',
        'marginBottom': '2em',
        'height': height,
        'display': 'block'}
)

sex_dropdown = dcc.Dropdown(
    id='sex-dropdown',
    options=[
        # label is what is shown up on the dropdown list
        {'label': 'Male', 'value': 'M'},
        {'label': 'Female', 'value': 'F'},
        {'label': 'Unknown', 'value': 'U'}
    ],
    # value='U',
    style={
        'width': '50%',
        'marginBottom': '2em',
        'height': height,
        },
    # clearable=False,
    # searchable=False,
    # multi=True,
    # place_holder='Select sex ...'
)

dob_date_picker = dcc.DatePickerSingle(
    id='dob-date-picker',
    min_date_allowed=datetime.datetime(1995, 8, 5),
    max_date_allowed=datetime.datetime.now().date(),
    initial_visible_month=datetime.datetime(2017, 8, 5),
    date=str(datetime.datetime.now().date()),
    style={
        'height': height,
        'fontSize': 6,
        'marginBottom': '4em',
        'marginRight': '2em'
    }
)

current_timestamp = dcc.Input(
    id='current-timestamp',
    type='text',
    placeholder='YYYY-mm-dd HH:MM:SS',
    value=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
    style={
        'width': '200px'
    }
)


# app.layout = html.Div([
#     # html.H6('subject_id'),
#     subject_id_input,
#     # html.H6('subject_nickname'),
#     subject_nickname_input,
#     # html.H6('sex'),
#     sex_dropdown,
#     # html.H6('dob'),
#     dob_date_picker
# ])

app.layout = html.Div(
    [
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.H6('Subject id'),
                        subject_id_input,
                        html.H6('Subject nickname'),
                        subject_nickname_input

                    ],
                    width=2

                ),
                dbc.Col(
                    [
                        html.H6('Sex'),
                        # dbc.Label('Sex'),
                        sex_dropdown,
                        html.H6('Date of birth'),
                        # dbc.Label(
                        #     'Date of birth',
                        #     style={
                        #         'marginRight': '1em'}),
                        dob_date_picker,
                        html.H6('Current Timestamp'),
                        #     'Current Timestamp',
                        #     style={
                        #         'marginRight': '1em'}),
                        current_timestamp
                    ]
                )
            ]
        ),
        dbc.Row(
            html.Div(['Hello world!'])
        )
    ]
)


if __name__ == '__main__':

    app.run_server(debug=True)
