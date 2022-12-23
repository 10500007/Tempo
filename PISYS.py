from requests.auth import HTTPBasicAuth
import requests
import pprint
import var


url_pi = 'https://piwebapi.edpbr.com.br/piwebapi/assetservers'

#from requests.auth import HTTPBasicAuth
#requests.get('https://api.github.com/user', auth=HTTPBasicAuth('user', 'pass'))

def requisicao(url):
    requisicao = requests.get(url, verify=False, timeout=200, auth=HTTPBasicAuth(var.login, var.passw))
    requisicao_json = requisicao.json()
    #pprint.pprint(requisicao_json)
    return requisicao_json


#######
assetservers_json = requisicao(url_pi)                                      #Pegando JSON geral da página
url_database = assetservers_json['Items'][0]['Links']['Databases']          #Filtrar Link database
assetdatabase_json = requisicao(url_database)                               #Retornando JSON do database
filtrar_controle_hidraulico = assetdatabase_json['Items'][3]                #Filtrando controle hidraulico em database
link_controle_hidraulico = filtrar_controle_hidraulico['Links']['Elements'] #Pegando url dos elementos de Controle. Hidr
url_elements_contr_hidr = link_controle_hidraulico
#######
contr_hidr_elements_json = requisicao(url_elements_contr_hidr)
filtrar_usina = contr_hidr_elements_json['Items'][5]
link_contr_hidr_ulaj = filtrar_usina['Links']['Attributes']
pprint.pprint(link_contr_hidr_ulaj)
