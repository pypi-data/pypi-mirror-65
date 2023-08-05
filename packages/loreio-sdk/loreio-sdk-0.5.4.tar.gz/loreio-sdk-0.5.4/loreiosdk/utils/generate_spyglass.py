from loreiosdk.spyglass_script import Spyglass

sp = Spyglass('wss://ui.getlore.io/storyteller', 'maurin', 'MA123$%',
              'tvfplay')

result = sp.cmd('help', raw=None)
print result

for cmd in result['data']:
    command_info = sp.cmd(cmd[0] + ' -h', yaml=None)
    print command_info
