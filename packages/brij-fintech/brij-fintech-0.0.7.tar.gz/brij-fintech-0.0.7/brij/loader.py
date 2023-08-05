
from brij.mpesa import MpesaService 
from brij.base import Auth
from brij import urls
import requests
from threading import Thread, Event
import time

class BrijLoader(Auth):
    def __init__(self, app_id, app_key):
        self.app_id = app_id
        self.app_key = app_key
        Auth.__init__(self, app_id=self.app_id, app_key=self.app_key)
         
    def get_mpesa_services(self):
        return MpesaService(app_id=self.app_id, app_key=self.app_key)
        
    def validate_mpesa_transaction(self, merchant_id, trans_type, timeout = 10):
        self.authenticate()
        
        stop_signal = Event()
        ob = {'response':None}
        def check_validity():
            while True:
                headers =  {'Authorization': 'Bearer {0}'.format(self.token), 'Content-Type': "application/json"}
                payload = {
                    'merchant_request_id':merchant_id,
                    'type':trans_type
                }
                response = requests.post(urls.mpesa_transaction_validation, json=payload, headers=headers)
                ob['response'] = response
                #print(response.json())
                
                if stop_signal.is_set():
                    break
                
                if response and response.json()['state'] == 'waiting':
                    time.sleep(5)
                    check_validity()
                elif response.json()['state'] == 'done':
                    stop_signal.set()
                    break
            
        thread = Thread(target=check_validity)
        thread.start()
        thread.join(timeout=timeout)
        stop_signal.set()
        
        return ob['response']
        

