from requests.auth import HTTPBasicAuth
import requests
import pprint
import var


controle_hidraulico_ulaj_afluente = 'https://piwebapi.edpbr.com.br/piwebapi/streams/F1AbEI133LfYSWkSxsaLVyoRvIg1kLmeax06BGBCABQVrohUgxdthc7kogFMosxTjD6X3BARURQQlIzMzlcQ09OVFJPTEUgSElEUkFVTElDT1xVTEFKfEFGTFVFTlRF/interpolated'


def requisicao(url):
    requisicao = requests.get(url, timeout=200, auth=HTTPBasicAuth(var.login, var.passw))
    requisicao_json = requisicao.json()
    return requisicao_json


req_json = requisicao(controle_hidraulico_ulaj_afluente)
pprint.pprint(req_json['Items'], indent=3)


