from time import sleep

from loreiosdk.spyglass_script import Spyglass


url = 'ws://dev01:10003/storyteller'
user = 'maurin'
pwd = 'MA123$%'


spyglass = Spyglass(url, user, pwd, dataset_id='tvfplay')

print(spyglass.cmd('ping'))

while True:
    sleep(1)
    try:
        print(spyglass.cmd('ping'))
    except:
        pass