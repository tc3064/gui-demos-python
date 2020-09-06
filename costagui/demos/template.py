import dash
import dash_table
import dash_html_components as html
import dash_core_components as dcc

app = dash.Dash(__name__)

app.layout = html.Div(
    [
        html.Div(id='container')
    ]
)

if __name__ == '__main__':

    app.run_server(debug=True)
