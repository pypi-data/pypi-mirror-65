
from brij.loader import BrijLoader

if __name__ == '__main__':
    loader = BrijLoader(app_id='NF0QqEDKG0blmNtGap0AXA==', app_key='dWGYyNuC7DIV+ogdtys4fVr+82NS9lH5')
    mpesa = loader.get_mpesa_services()
    response = mpesa.mpesa_to_acc(1, 'Brian', '254706033970', 'test to acc')
    print(response.json())
    r = loader.validate_mpesa_transaction(response.json()['MerchantRequestID'], 'direct')
    print(r.json())