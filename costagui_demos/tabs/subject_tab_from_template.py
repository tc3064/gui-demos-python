import datajoint as dj
from costagui_demos.dj_tables import lab, subject
from costagui_demos.app import app
from dj_dashboard.templates import TableBlock


subject_table_tab = TableBlock(
    subject.Subject, app,
    extra_tables=[subject.Subject.User, subject.Subject.Protocol])


if __name__ == '__main__':
    dj.config['safemode'] = False
    app.layout = subject_table_tab.layout
    app.run_server(debug=True)
