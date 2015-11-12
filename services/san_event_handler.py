import subprocess
from settings import COLLECT_CHANGES_SCRIPT

try:
    from settings import ALLOWED_CFGENABLE_SENDERS as SENDERS
except:
    SENDERS = '__all__'

def handle(message):
    event = message.get('event', '')
    data = message.get('data', {})
    if event == 'test':
        print('Test signal received: {}'.format(message))
    elif event == 'cfgenable':
        sender = data.get('sender') or data.get('serial')
        if type(SENDERS) == list and sender in SENDERS:
            subprocess.Popen(
                ['/usr/bin/python3', COLLECT_CHANGES_SCRIPT],
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
            )
            print('cfgenable OK')
            

