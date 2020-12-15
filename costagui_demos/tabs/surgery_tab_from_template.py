# %%
import datajoint as dj
from costagui_demos.dj_tables import subject, lab, surgery
from costagui_demos.app import app
from dj_dashboard.templates import TableBlock

# %%
surgery_table_tab = TableBlock(
    surgery.Surgery, app,
    extra_tables=[surgery.Surgery.Implant,
                  surgery.Surgery.Pipette,
                  surgery.Surgery.Injection])


if __name__ == '__main__':
    dj.config['safemode'] = False
    app.layout = surgery_table_tab.layout
    app.run_server(debug=True)

# %%
