import requests
import pprint
import urllib.parse

url_1 = 'https://www.netclima.com.br/php/hi/netclima_recuperahida.php?parametros={'
url_2 = '"modo":4,"datainicio":"2022-12-08 13:53:49","datatermino":"2022-12-12 14:53:49","valorpomenor":"0","valorpomaior":"0","valornemenor":"0","valornemaior":"0","filtrodans":true,"filtrodain":true,"filtrocopo":true,"filtrocone":true,"concessao":true,"dado":true,"exporta":0,"selecionado":{"elemelemento":"SE UHE São Manoel","elemcamadagis":"subestacaotemp","elemcampo":"nome","elembuffer":"5000","elemtipo":"1","elemns":"55","elemin":"66","elemto":"121","elemtipocampo":"0","elemdataanalise":"2020-01-01 00:00:00","elemtipoanalise":"0"},"GeoJSON":true,"GeoJSONBuffer":false'
url_entidade='}&entidade=EDP_T'

encodedStr = url_2
#conv = urllib.parse.unquote(encodedStr)
#converter formato para link final da url
url_conv = urllib.parse.quote(encodedStr).replace('%3A',':').replace('%2C',',')

url_final = url_1 +''+ url_conv+''+url_entidade
print(url_final)

req = requests.get(url_final, verify=False)
meu_json_req = req.json()
pprint.pprint(meu_json_req, indent=4)
