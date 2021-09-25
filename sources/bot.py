# from sources.telega import Settings
import callUtils
import requests
import json
from requests import HTTPError

Settings = None


class GrotemServerConnector(object):

    def __init__(self, url='', password=''):
        self._server_url = url
        self._server_password = password

    def _send_command(self, uri, **kwargs):
        url = self._server_url + uri
        passwd = kwargs['auth_password'] if 'auth_password' in kwargs else self._server_password

        try:
            response = requests.get(url=url, auth=('admin', passwd))
            response.raise_for_status()
        except HTTPError as http_err:
            return f'{http_err}'
        except Exception as err:
            return f'{err}'
        else:
            return response.text

    def _get_solution_password(self, solution_name):
        if solution_name is None:
            raise ValueError('Solution Name required')
        pet_password_uri = f'/system/solutions/getpassword/{solution_name}'
        result = self._send_command(pet_password_uri)
        return result

    def check_connection(self):
        check_uri = '/system/version'
        response = self._send_command(check_uri)
        if '(ver ' in response:
            return 0
        else:
            print(response)
            return -1

    def get_lic_info(self, solution_name: str):
        if solution_name is None:
            raise ValueError('Solution Name required')

        glic_uri = f'/{solution_name}/admin/GetLicensesCount'
        solution_password = self._get_solution_password(solution_name)
        result = self._send_command(glic_uri, auth_password=solution_password)

        if type(result) != str:
            return {'status': 1, 'details': 'Get licenses error: '+str(result)}

        try:
            lic_info = json.loads(result)
        except Exception as e:
            return {'status': 2, 'details': 'Get licenses error: ' + str(e)}

        return {'status': 0, 'details': '', 'licenses': lic_info}

    def set_lic_count(self, solution_name: str, lic_count: int):
        if solution_name is None:
            raise ValueError('Solution Name required')

        slic_uri = f'/system/solutions/setlicenses/{solution_name}/{lic_count}'
        return self._send_command(slic_uri)


    def reset_lic_count(self, solution_name: str):
        return True


def init():
    if Settings != None:
        callUtils.rootPassword = Settings['rootPassword']
        callUtils.utilsPath = Settings['UtilsPath']
        callUtils.bitmobileHost = Settings['bitmobileHost']

def glic(sn, sp=None):
    if sp == None:
        sp = callUtils.getSP(sn)
    if sp != None:
        UtilsOutput = str(callUtils.getLics(sn, sp))        
        if UtilsOutput.find('Invalid')==-1:
            return UtilsOutput.replace("b'{", '').replace("}\\r\\n\'", '')        
        else:
            return "not found"
    else:
        return "not found"    


def slic(sn):
    sp = callUtils.getSP(sn)
    if sp != None:
       UtilsOutput = str(callUtils.getLics(sn, sp))
       if UtilsOutput.find('Invalid')==-1:
            TotalLicenses = UtilsOutput.split(',')
            licCount = int(TotalLicenses[0][TotalLicenses[0].find(":")+1:]) 
            callUtils.slic(sn, licCount)
            return glic(sn, sp)
       else:
            return "not found"
    else:
        return "not found"

 
       
