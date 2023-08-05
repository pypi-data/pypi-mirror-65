#!C:\Python38\python.exe
# EASY-INSTALL-ENTRY-SCRIPT: 'wait-for-amqp==1.0','console_scripts','wait-for-amqp'
__requires__ = 'wait-for-amqp==1.0'
import re
import sys
from pkg_resources import load_entry_point

if __name__ == '__main__':
    sys.argv[0] = re.sub(r'(-script\.pyw?|\.exe)?$', '', sys.argv[0])
    sys.exit(
        load_entry_point('wait-for-amqp==1.0', 'console_scripts', 'wait-for-amqp')()
    )
