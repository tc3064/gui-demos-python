import datajoint as dj
dj.config['database.host'] = 's1n4.u19motor.zi.columbia.edu'
dj.config['database.user'] = 'RuiLab_test'
dj.config['database.password'] = 'test1'

lab = dj.create_virtual_module('lab', 'costa_lab')
subject = dj.create_virtual_module('subject', 'costa_subject')
action = dj.create_virtual_module('action', 'costa_action')
acquisition = dj.create_virtual_module('acquisition', 'costa_acquisition')
hardware = dj.create_virtual_module('hardware', 'costa_hardware')
