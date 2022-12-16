import requests
import pprint
import urllib.parse
import urllib3.connection
import urls_localidades
from haversine import haversine


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
print(len(requisicao_json['features'])) #tamanho do array que contem eventos
#pprint.pprint(requisicao_json['features'][0]['geometry'], indent=4)

tamanho_array = len(requisicao_json['features'])
contador = 1
for i in range(tamanho_array):
    #pprint.pprint(requisicao_json['features'][i]['properties'], indent=4)
    coord = 'Evento',i,requisicao_json['features'][i]['geometry']['coordinates']
    data_hora = requisicao_json['features'][i]['properties']['dat_data']
    flag_nuvem = requisicao_json['features'][i]['properties']['dat_flag_intranuvem']
    coord_lat = coord[2][1] 
    coord_long = coord[2][0]   
    #print('Evento',i,requisicao_json['features'][i]['geometry']['coordinates'][0])
    #print('latitude',coord_lat,'longitude',coord_long)
    peixe_angical = (-12.2311, -48.3891) # (lat, lon)
    coord_do_event = (coord_lat, coord_long)
    distancia_calculada = haversine(peixe_angical, coord_do_event)
    #print(distancia_calculada)

    if distancia_calculada<750:
        print('Evento - ',contador,'-',distancia_calculada,'-',data_hora,'-',flag_nuvem)
        contador = contador + 1