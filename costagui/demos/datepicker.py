import dash
import dash_table
import dash_html_components as html
import dash_core_components as dcc
import datetime


app = dash.Dash(__name__)

dob_date_picker = dcc.DatePickerSingle(
    id='dob-date-picker',
    min_date_allowed=datetime.datetime(1995, 8, 5),
    max_date_allowed=datetime.datetime.now().date(),
    initial_visible_month=datetime.datetime(2020, 3, 5),
    # date=str(datetime.datetime.now().date()),
    style={
        'width': '150px',
        'marginBottom': '2em'
    }
)

timestamp_picker = dcc.Input(
    id='timestamp-picker',
    type='text',
    placeholder='YYYY-mm-dd HH:MM:SS',
    value=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
    style={
        'width': '150px'
    }
)


app.layout = html.Div([
    html.Div(children='Date of birth'),
    dob_date_picker,
    html.Div(children='Start Time'),
    timestamp_picker
])


if __name__ == '__main__':

    app.run_server(debug=True)
