from requests.auth import HTTPBasicAuth
import requests
import pprint
import var


url = 'https://piwebapi.edpbr.com.br/piwebapi/attributes?'


def requisicao(url):
    requisicao = requests.get(url, timeout=200, auth=HTTPBasicAuth(var.login, var.passw), path='\\EDPBR339\SAMUG\SAMUG\ULAJ\UG01|Estado Operativo COG')
    requisicao_json = requisicao.json()
    return requisicao_json


req_json = requisicao(url)
pprint.pprint(req_json)


