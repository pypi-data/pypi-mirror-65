import requests
from brij import Auth
from brij import urls

class MpesaServices(Auth):
    
    def __init__(self, env='sandbox', app_id=None, app_key=None):
        Auth.__init__(self, env, app_id, app_key)
        self.authenticate()
        
    def mpesa_to_acc(self, amount, sender, sender_phone, description=None):
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
        
        headers = {'Authorization': 'Bearer {0}'.format(self.token), 'Content-Type': "application/json"}
        mpesa_to_acc_url = '{}{}'.format(urls.base_url, urls.mpesa_to_acc_url)
        r = requests.post(mpesa_to_acc_url, headers=headers, json=payload)
        
        return r
        
    def mpesa_to_escrow(self, amount, sender, recepient, sender_phone, description=None):
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
        
        headers = {'Authorization': 'Bearer {0}'.format(self.token), 'Content-Type': "application/json"}
        
        mpesa_to_escrow_url = '{}{}'.format(urls.base_url, urls.mpesa_to_escrow_url)
        
        r = requests.post(mpesa_to_escrow_url, headers=headers, json=payload)
        
        return r
        
        
        