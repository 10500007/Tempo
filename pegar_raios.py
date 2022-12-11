import requests
import json

UserPass = 'edp_benedito:5sux5Q4iQA'
lat_sp = '-23.5489'
long_sp = '-46.6388'
lat_jari= '-0.651026'
long_jari ='-52.532597'
lat_peixe ='-12.2351062'
long_peixe = '-48.3886669'
data_hora = '2022-12-11T11:00:00Z'



url_1 = 'https://'+UserPass+'@api.meteomatics.com/'+data_hora+'/lightning_strikes_10km_24h:x/'+lat_sp+','+long_sp+'/json'
url_2 = 'https://'+UserPass+'@api.meteomatics.com/'+data_hora+'/lightning_strikes_10km_24h:x/'+lat_jari+','+long_jari+'/json'
url_3 = 'https://'+UserPass+'@api.meteomatics.com/'+data_hora+'/lightning_strikes_10km_24h:x/'+lat_peixe+','+long_peixe+'/json'

array_url = [url_1,url_2,url_3]

cont = 0
for i in array_url:
    cont = cont + 1
    url = i
    req = requests.get(url)   
    meu_json_req = req.json()
    print(meu_json_req)    
print('fim for')

#print(url)
#req = requests.get(url)
#print(req.json())
#meu_json_req = req.json()
#load_meu_json = json.load(meu_json_req)
#var1 = meu_json_req['data']
#var2 = var1[0]['coordinates']
#var3 = var2[0]['dates']
#var4 = var3[0]['value']

#print(var4)
