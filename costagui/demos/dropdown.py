import dash
import dash_core_components as dcc
import dash_html_components as html

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)


sex_dropdown = dcc.Dropdown(
    id='sex-dropdown',
    options=[
        # label is what is shown up on the dropdown list
        {'label': 'Male', 'value': 'M'},
        {'label': 'Female', 'value': 'F'},
        {'label': 'Unknown', 'value': 'U'}
    ],
    # value='U',
    style={'width': '500px'},
    # clearable=False,
    # searchable=False,
    multi=True,
    placeholder='Select sex ...'
)

app.layout = html.Div(
    children=[sex_dropdown]
)

if __name__ == '__main__':
    app.run_server(debug=True)
