import requests
from brij.base import Auth
from brij import urls

class MpesaService(Auth):
    
    def __init__(self, env='sandbox', app_id=None, app_key=None):
        Auth.__init__(self, env, app_id, app_key)
        
    def get_headers(self):
        return {'Authorization': 'Bearer {0}'.format(self.token), 'Content-Type': "application/json"}
        
    def mpesa_to_acc(self, amount, sender, sender_phone, description=None):
        self.authenticate()
        '''
        this method uses MPESA API to send cash from your app user to your account in brij.
        **Args:*"
        -amount (int) amount to be sent
        -sender (str) the unique id of your user
        -description (str) reason for sending
        -sender_phone (str) phone number sending the cash starting with the country code without the plus sign
        
        **returns:**
        
        
        '''
        payload= {
            'env':self.env,
            'amount':amount,
            'sender':sender,
            'description': description,
            'phone_number':sender_phone
        }
        
        headers = self.get_headers()
        mpesa_to_acc_url = urls.mpesa_to_acc_url
        r = requests.post(mpesa_to_acc_url, headers=headers, json=payload)
        
        return r
        
    def mpesa_to_escrow(self, amount, sender, recepient, sender_phone, description=None):
        self.authenticate()
        '''
        this method uses MPESA API to escrow cash between your app users, using your Brij account as the escrow account
        ***Args***
        -amount (string) 
        -sender (string) sender email address or Mpesa phone number starting with the country code without the plus sign
        -recepient (string) recepient email address or Mpesa phone number starting with the country code without the plus sign
        -description (string) reason for sending
        '''
        payload = {
            'amount':amount,
            'sender':sender,
            'recepient':recepient,
            'phone_number':sender_phone,
            'description':description
        }
        
        headers = self.get_headers()
        
        mpesa_to_escrow_url = urls.mpesa_to_escrow_url
        
        r = requests.post(mpesa_to_escrow_url, headers=headers, json=payload)
        
        return r
        
    def get_all_transactions(self):
        self.authenticate()
        '''
        this method requests all mpesa transactions from brij platform
        '''
        headers = self.get_headers()
        
        r = requests.get(urls.all_direct_trans, headers=headers)
        trans = list()
        trans = trans + r
        
        r = requests.get(urls.all_escrow_trans, headers=headers)
        trans=trans+r
        
        return jsonify(trans)
        
    def get_all_direct_transactions(self):
        self.authenticate()
        '''
        gets all direct mpesa direct transactions
        '''
        headers = self.get_headers()
        r = requests.get(urls.all_direct_trans, headers=headers)
        return trans
        
    def get_all_escrow_trans(self):
        self.authenticate()
        '''
        gets all mpesa escrow get_all_direct_transactions
        '''
        
        headers = self.get_headers()
        r = requests.get(urls.all_escrow_trans, headers=headers)
        return r
        
        
    def get_direct_trans_by_merchant_id(self, merchant_id):
        self.authenticate()
        
        payload = {
            'merchant_id':merchant_id
        }
        
        r = requests.get(urls.direct_trans_by_merchant_id, json=payload, headers=self.get_headers())
        return r
        
        
    def get_direct_trans(self, trans_id):
        self.authenticate()
        
        payload = {
            'trans_id':trans_id
        }
        
        r = requests.get(urls.direct_trans_by_id, json=payload, headers=self.get_headers())
        
        return r
        
    def get_escrow_trans(self, trans_id):
        self.authenticate()
        
        payload = {
            'trans_id':trans_id
        }
        r = requests.get(urls.escrow_trans_by_id, json=payload, headers = self.get_headers())
        return r
        
        
    def get_escrow_trans_by_merchant_id(self, merchant_id):
        self.authenticate()
        
        payload = {
            'merchant_id':merchant_id
        }
        
        r = requests.get(urls.escrow_trans_by_merchant_id, json=payload, headers=self.get_headers())
        return r
        
        