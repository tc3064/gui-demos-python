import dash
import dash_bootstrap_components as dbc
import dash_html_components as html
from dash.dependencies import Input, Output

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = html.Div(
    [
        dbc.DropdownMenu(
            [
                dbc.DropdownMenuItem("Header1", header=True),
                dbc.DropdownMenuItem("Button 1", id="button-1"),
                dbc.DropdownMenuItem("Botton 2", id="botton-2")
            ],
            label="Menu",
        ),
        html.P(id="item-clicks", className="mt-3"),
    ]
)


@app.callback(
    Output("item-clicks", "children"), [Input("button-1", "n_clicks")]
)
def count_clicks(n):
    if n:
        return f"Button clicked {n} times."
    return "Button not clicked yet."


if __name__ == '__main__':

    # run the server, debug = True allows auto-updating without restarting the server.
    app.run_server(debug=True)
