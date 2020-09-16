import datajoint as dj

lab = dj.create_virtual_module('lab', 'costa_lab')
subject = dj.create_virtual_module('subject', 'costa_subject')


# insert some sample data for development

lab.User.insert(
    [['shans', 'Shan Shen', 'shanshen@vathes.com', '000-000-0000']],
    skip_duplicates=True
)

subject.Subject.insert([
    ['mouse1', 'shan-mouse1', 'NA', 'F', '2019-08-27', 'ear', 'LL', None, None, 'GCaMP6s', 'JAX', '', None],
    ['mouse2', 'shan-mouse2', 'NA', 'M', '2019-08-27', 'ear','RR', None, None, 'PV-Ai9', 'JAX', '', None],
    ['mouse3', 'shan-mouse3', 'NA', 'U', '2019-08-27', 'ear','LR', None, None, 'GCaMP6s', 'JAX', '', None],
    ['mouse4', 'shan-mouse4', 'NA', 'M', '2019-08-27', '','', None, None, None, 'JAX', '', None],
    ['mouse5', 'mouse5', 'NA', 'M', '2019-08-27', '','', None, None, None, 'JAX', '', None],

], skip_duplicates=True)

subject.Subject.User.insert([
    ['mouse1', 'shans'],
    ['mouse2', 'shans'],
    ['mouse3', 'shans'],
    ['mouse4', 'shans'],
    ['mouse5', 'acm2246']
], skip_duplicates=True)

subject.Subject.Protocol.insert([
    ['mouse1', '2020-09-10', 'AABE7561'],
    ['mouse2', '2020-09-10', 'AABE7561'],
    ['mouse3', '2020-09-10', 'AABG0559'],
    ['mouse4', '2020-09-10', 'AABG0559'],
    ['mouse5', '2020-09-10', 'AABG0559'],
], skip_duplicates=True)
