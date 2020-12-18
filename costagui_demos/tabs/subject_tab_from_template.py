import datajoint as dj
from costagui_demos.app import app
from dj_dashboard.templates import TableBlock
from costagui_demos.dj_tables import lab, subject


tab = TableBlock(
        subject.Subject, app,
        extra_tables=[subject.Subject.User, subject.Subject.Protocol])


if __name__ == '__main__':
    dj.config['safemode'] = False
    app.layout = tab.layout
    app.run_server(debug=True)
