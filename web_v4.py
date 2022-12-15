import requests
import pprint
import urllib.parse
import urllib3.connection
import urls_localidades

url_fixo = 'https://www.netclima.com.br/php/hi/netclima_recuperahida.php?parametros={'
url_parametros = urls_localidades.url_tocantins_2
url_entidade='}&entidade=EDP_T'

encodedStr = url_parametros
#conv = urllib.parse.unquote(encodedStr)
#converter formato para link final da url
url_convert = urllib.parse.quote(encodedStr).replace('%3A',':').replace('%2C',',')

url_final = url_fixo +''+ url_convert+''+url_entidade
#print(url_final)
requisicao = requests.get(url_final, verify=False, timeout=2000)
requisicao_json = requisicao.json()
print(len(requisicao_json['features'][0]))
#pprint.pprint(requisicao_json['features'][0]['geometry'], indent=4)


for i in range(10):
    pprint.pprint(requisicao_json['features'][i]['geometry'], indent=4)
