# vers anterior AML2310.py
import json
import os

from urllib3.util.retry import Retry
from requests import Session
from requests.adapters import HTTPAdapter

from ._dict_urlData import dict_urlData

url_base = 'https://alchemyml.com/api'

def retry_session(retries, session = None, backoff_factor = 0.3, 
                  status_forcelist = (500, 502, 503, 504)):
    session = session or Session()
    retry = Retry(
        total = retries,
        read = retries,
        connect = retries,
        backoff_factor = backoff_factor,
        status_forcelist = status_forcelist,
    )
    adapter = HTTPAdapter(max_retries = retry)
    session.mount('http://', adapter)
    session.mount('https://', adapter)
    return session

def general_call(self, str_meth_name, input_args, input_kwargs):
    if str_meth_name in dict_urlData.keys():
        if hasattr(self, 'token'):
            api_token = self.token
        else:
            api_token = ''

        urlData = url_base + dict_urlData[str_meth_name]
        headers = {'Authorization': 'Bearer ' + api_token}
                
        if input_args:
            input_kwargs['args'] = input_args
            
        mi_data = input_kwargs
        
        if not 'file_path' in input_kwargs.keys():
            headers['Content-type'] = 'application/json'
            session = retry_session(retries = 10)
            api_request = session.post(urlData, headers = headers, json = mi_data)

        else:
            file_path = input_kwargs['file_path']
            del input_kwargs['file_path']
            
            if os.path.exists(file_path):
                file_last_modif_date = int(round(os.stat(file_path).st_mtime))
            else:
                reply = {'success': False,
                          'status_code':'',
                          'message': 'Result Upload SCRIPT: File not found - NOT valid file path.',
                          'data': {'invalid input': 'File not found - NOT valid file path.'}}
                return reply
            if str_meth_name == 'dataset.upload':
                mi_data["last_modification_date"] = file_last_modif_date
            files = {'file_path': open(file_path, 'rb')}
            session = retry_session(retries=10)
            api_request = session.post(urlData, headers = headers, 
                                       files = files, data = mi_data)
        
        res_json = json.loads(api_request.text)
        res_json_return = res_json.copy()
        res_json_return['status_code'] = api_request.status_code
        if api_request.status_code == 200:
            if 'data' in res_json.keys():
                if isinstance(res_json['data'], dict ) and ('url' in res_json['data'].keys()):
                    session = retry_session(retries=10)
                    r = session.get(res_json['data']['url'])
                    f_name = str(res_json['data']['url']).split("/")[-1]
                    open(f_name, 'wb').write(r.content)

                    return 'File '+ f_name + ' successfully generated.'
                
                else:
                    return res_json_return

            else:
                return res_json_return
    
        else:
            return res_json_return
    