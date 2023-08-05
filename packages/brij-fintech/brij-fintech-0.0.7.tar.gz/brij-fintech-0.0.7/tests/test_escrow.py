from mpesa import MpesaService

if __name__ == '__main__':
    service = MpesaService(app_id='NF0QqEDKG0blmNtGap0AXA==', app_key='dWGYyNuC7DIV+ogdtys4fVr+82NS9lH5')
    r = service.mpesa_to_escrow('50', 'brianmuigai1@gmail.com', 'janshiroz@gmail.com', '254706033970', 'test escrow')
    print(r.json())