from mpesa import MpesaService

if __name__ == '__main__':
    to_acc = MpesaService(app_id='NF0QqEDKG0blmNtGap0AXA==', app_key='dWGYyNuC7DIV+ogdtys4fVr+82NS9lH5')
    r = to_acc.mpesa_to_acc(50, 'Brian', '254706033970', 'test to acc')
    if r:
        print(r.text)
    else:
        print('error')