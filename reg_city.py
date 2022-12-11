import requests
import json 

#locales = {'username': 'meuusername123', 'password': 'senha1234'} #1

resposta = requests.post("http://apiadvisor.climatempo.com.br/api-manager/user-token/1b82cef44478dd60dcdc9f9f86a7513f/locales", locales=3477) #2

print(iRETORNO_REQ)