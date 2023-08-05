from auth import BrijBase
from flask import jsonify

if __name__ == '__main__':
    base = BrijBase(app_id='NF0QqEDKG0blmNtGap0AXA==', app_key='dWGYyNuC7DIV+ogdtys4fVr+82NS9lH5')
    r = base.authenticate()
    print(r)