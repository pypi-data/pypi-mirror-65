
#base_url = 'http://localhost:8080/'

base_url = 'https://brij-tech.herokuapp.com/'
tokens = base_url+'api/tokens'
mpesa_to_acc_url = base_url+'api/mpesa-to-acc'
mpesa_to_escrow_url = base_url+'api/mpesa-to-escrow'
all_direct_trans = base_url+'api/get-all-direct-trans'
all_escrow_trans = base_url+'api/get-all-escrow-trans'
direct_trans_by_id = base_url+'api/get-direct-trans-by-id'
direct_trans_by_merchant_id=base_url+'api/get-direct-trans-by-merchant-id'
escrow_trans_by_id = base_url+'api/get-escrow-trans-by-id'
escrow_trans_by_merchant_id = base_url+'api/get-escrow-trans-by-merchant-id'
mpesa_transaction_validation = base_url+'api/check-trans-validity'