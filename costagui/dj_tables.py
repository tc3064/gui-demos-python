import datajoint as dj

lab = dj.create_virtual_module('lab', 'costa_lab')
subject = dj.create_virtual_module('subject', 'costa_subject')
action = dj.create_virtual_module('action', 'costa_action')
acquisition = dj.create_virtual_module('acquisition', 'costa_acquisition')
hardware = dj.create_virtual_module('hardware', 'costa_hardware')
