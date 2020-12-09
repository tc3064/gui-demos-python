import datajoint as dj
import dash
import dash_table
from dash.dependencies import Input, Output, State
import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc
from costagui_demos.app import app
from costagui_demos.dj_tables import lab, subject, hardware
from costagui_demos import dj_utils, component_utils, callback_utils
from costagui_demos.tab_templates import TableBlock
import datetime


subject_table_tab = TableBlock(hardware.Computer, app)


if __name__ == '__main__':
    dj.config['safemode'] = False
    app.layout = subject_table_tab.layout
    app.run_server(debug=True)
