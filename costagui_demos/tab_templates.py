import datajoint as dj
import dash
import dash_table
from dash.dependencies import Input, Output, State
import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc
from costagui_demos.dj_tables import lab, subject, hardware
from costagui_demos import dj_utils, component_utils, callback_utils
import datetime

DataJointTable = dj.user_tables.OrderedClass


class TableBlock:
    def __init__(self, table: DataJointTable, app=None, include_parts=False,
                 table_height='800px',
                 table_width='800px',
                 button_style={
                    'marginRight': '1em',
                    'marginBottom': '1em'},
                 messagebox_style={
                    'width': 750,
                    'height': 50,
                    'marginBottom': '1em',
                    'display': 'block'},
                 ):
        self.app = app
        self.table = table
        self.table_name = table.__name__.lower()
        self.primary_key = table.heading.primary_key
        self.attrs = table.heading.attributes

        self.display_table = component_utils.create_display_table(
            table, f'{self.table_name}-table',
            height=table_height, width=table_width)

        self.add_button = html.Button(
            children=f'Add a {self.table_name} record',
            id=f'add-{self.table_name}-button', n_clicks=0,
            style=button_style)

        self.delete_button = html.Button(
            children=f'Delete the current record',
            id=f'delete-{self.table_name}-button', n_clicks=0,
            style=button_style
        )

        self.update_button = html.Button(
            children='Update the current record',
            id=f'update-{self.table_name}-button', n_clicks=0,
            style=button_style
        )

        self.add_modal = component_utils.create_modal(
            table, self.table_name, include_parts=include_parts,
            mode='add'
        )

        self.update_modal = component_utils.create_modal(
            table, self.table_name, include_parts=include_parts,
            mode='update'
        )

        self.delete_message_box = dcc.Textarea(
            id=f'delete-{self.table_name}-message-box',
            value=f'Delete {self.table_name} message:',
            style=messagebox_style
        )

        self.delete_confirm = dcc.ConfirmDialog(
            id=f'delete-{self.table_name}-confirm',
            message='Are you sure to delete the record?',
        ),

        if self.app is not None and hasattr(self, 'callbacks'):
            self.callbacks(self.app)

    def create_default_layout(self):
        self.layout = html.Div(
            html.Div(
                className="row app-body",
                children=[
                    html.Div(
                        [
                            html.Div(
                                [
                                    html.Div(
                                        [
                                            html.Div(
                                                self.add_button,
                                                style={'display': 'inline-block'}),
                                            html.Div(
                                                self.delete_button,
                                                style={'display': 'inline-block'}),
                                            html.Div(
                                                self.update_button,
                                                style={'display': 'inline-block'})
                                        ],
                                    ),
                                    self.delete_message_box,
                                ]
                            ),

                            html.Div(
                                [
                                    html.H6('Subject'),
                                    self.display_table
                                ],
                                style={'marginRight': '1em',
                                       'display': 'inline-block'}),
                        ]
                    ),
                    # confirmation dialogue
                    html.Div(self.delete_confirm),
                    # modals
                    self.update_modal,
                    self.add_modal
                ]
            )
        )

    def callbacks(self, app):

        @app.callback(
            Output(f'delete-{self.table_name}-confirm', 'displayed'),
            [Input(f'delete-{self.table_name}-button', 'n_clicks')])
        def display_confirm(n_clicks):
            if n_clicks:
                return True
            return False

        @app.callback(
            [
                Output(f'{self.table_name}-table', 'data'),
                Output(f'delete-{self.table_name}-message-box', 'value')
            ],
            [
                Input(f'add-{self.table_name}-close', 'n_clicks'),
                Input(f'delete-{self.table_name}-confirm', 'submit_n_clicks'),
                Input(f'update-{self.table_name}-close', 'n_clicks'),
                Input(f'{self.table_name}-table', 'selected_rows')
            ],
            [
                State(f'{self.table_name}-table', 'data'),
            ]
        )
        def update_table_data(
                n_clicks_add_close, n_clicks_delete, n_clicks_update_close,
                selected_rows, data):

            delete_message = 'Delete subject message:\n'
            ctx = dash.callback_context
            triggered_component = ctx.triggered[0]['prop_id'].split('.')[0]

            if triggered_component == f'delete-{self.table_name}-confirm' and selected_rows:
                current_record = callback_utils.clean_single_gui_record(
                    data[selected_rows[0]], self.attrs)
                pk = {k: v for k, v in current_record.items()
                      if k in self.primary_key}
                try:
                    (self.table & pk).delete()
                    delete_message = delete_message + \
                        f'Successfully deleted record {pk}!'
                except Exception as e:
                    delete_message = delete_message + \
                        f'Error in deleting record {pk}: {str(e)}.'

            data = self.table.fetch(as_dict=True)

            return data, delete_message
