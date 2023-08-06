#!D:\workspace\virtualenv\dictfire-HRrbf1dM\Scripts\python.exe
# EASY-INSTALL-ENTRY-SCRIPT: 'dictfire==1.0.15','console_scripts','dict'
__requires__ = 'dictfire==1.0.15'
import re
import sys
from pkg_resources import load_entry_point

if __name__ == '__main__':
    sys.argv[0] = re.sub(r'(-script\.pyw?|\.exe)?$', '', sys.argv[0])
    sys.exit(
        load_entry_point('dictfire==1.0.15', 'console_scripts', 'dict')()
    )
