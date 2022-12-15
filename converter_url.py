import requests
import pprint
import urllib.parse

url = 'https://www.netclima.com.br/php/hi/netclima_recuperahida.php?parametros={%22modo%22:4,%22datainicio%22:%222022-12-01%2013:53:49%22,%22datatermino%22:%222022-12-12%2014:53:49%22,%22valorpomenor%22:%220%22,%22valorpomaior%22:%220%22,%22valornemenor%22:%220%22,%22valornemaior%22:%220%22,%22filtrodans%22:true,%22filtrodain%22:true,%22filtrocopo%22:true,%22filtrocone%22:true,%22concessao%22:true,%22dado%22:true,%22exporta%22:0,%22selecionado%22:{%22elemelemento%22:%22SE%20UHE%20S%C3%A3o%20Manoel%22,%22elemcamadagis%22:%22subestacaotemp%22,%22elemcampo%22:%22nome%22,%22elembuffer%22:%225000%22,%22elemtipo%22:%221%22,%22elemns%22:%2255%22,%22elemin%22:%2266%22,%22elemto%22:%22121%22,%22elemtipocampo%22:%220%22,%22elemdataanalise%22:%222020-01-01%2000:00:00%22,%22elemtipoanalise%22:%220%22},%22GeoJSON%22:true,%22GeoJSONBuffer%22:false}&entidade=EDP_T'

url_2 = 'https://www.netclima.com.br/php/hi/netclima_recuperahida.php?parametros={%22modo%22:4,%22datainicio%22:%222022-12-01%2013:53:49%22,%22datatermino%22:%222022-12-12%2014:53:49%22,%22valorpomenor%22:%220%22,%22valorpomaior%22:%220%22,%22valornemenor%22:%220%22,%22valornemaior%22:%220%22,%22filtrodans%22:true,%22filtrodain%22:true,%22filtrocopo%22:true,%22filtrocone%22:true,%22concessao%22:true,%22dado%22:true,%22exporta%22:0,%22selecionado%22:{%22elemelemento%22:%22SE%20UHE%20Cachoeira%20Caldeir%C3%A3o%22,%22elemcamadagis%22:%22subestacaotemp%22,%22elemcampo%22:%22nome%22,%22elembuffer%22:%225000%22,%22elemtipo%22:%221%22,%22elemns%22:%222%22,%22elemin%22:%221%22,%22elemto%22:%223%22,%22elemtipocampo%22:%220%22,%22elemdataanalise%22:%222020-01-01%2000:00:00%22,%22elemtipoanalise%22:%220%22},%22GeoJSON%22:true,%22GeoJSONBuffer%22:false}&entidade=EDP_T'

url_tocantins = 'https://www.netclima.com.br/php/hi/netclima_recuperahida.php?parametros={%22modo%22:4,%22datainicio%22:%222022-12-14%2012:28:03%22,%22datatermino%22:%222022-12-15%2013:28:03%22,%22valorpomenor%22:%220%22,%22valorpomaior%22:%220%22,%22valornemenor%22:%220%22,%22valornemaior%22:%220%22,%22filtrodans%22:true,%22filtrodain%22:true,%22filtrocopo%22:true,%22filtrocone%22:true,%22concessao%22:true,%22dado%22:true,%22exporta%22:0,%22selecionado%22:{%22elemelemento%22:%22Tocantins%22,%22elemcamadagis%22:%22estados%22,%22elemcampo%22:%22nome%22,%22elembuffer%22:%220.00001%22,%22elemtipo%22:%220%22,%22elemns%22:%2212.586%22,%22elemin%22:%2233%22,%22elemto%22:%2242.626%22,%22elemtipocampo%22:%220%22,%22elemdataanalise%22:%222020-01-01%2000:00:00%22,%22elemtipoanalise%22:%220%22},%22GeoJSON%22:true,%22GeoJSONBuffer%22:false}&entidade=EDP_T'

url_3 = 'https://www.netclima.com.br/php/hi/netclima_recuperahida.php?parametros={%22modo%22:4,%22datainicio%22:%222022-12-15%2013:34:55%22,%22datatermino%22:%222022-12-15%2014:34:55%22,%22valorpomenor%22:%220%22,%22valorpomaior%22:%220%22,%22valornemenor%22:%220%22,%22valornemaior%22:%220%22,%22filtrodans%22:true,%22filtrodain%22:true,%22filtrocopo%22:true,%22filtrocone%22:true,%22concessao%22:true,%22dado%22:false,%22exporta%22:0,%22selecionado%22:{%22elemelemento%22:%22Tocantins%22,%22elemcamadagis%22:%22estados%22,%22elemcampo%22:%22nome%22,%22elembuffer%22:%220.00001%22,%22elemtipo%22:%220%22,%22elemns%22:%22444%22,%22elemin%22:%22858%22,%22elemto%22:%221.302%22,%22elemtipocampo%22:%220%22,%22elemdataanalise%22:%222020-01-01%2000:00:00%22,%22elemtipoanalise%22:%220%22},%22GeoJSON%22:true,%22GeoJSONBuffer%22:false}&entidade=EDP_T'

encodedStr = url_3
conv = urllib.parse.unquote(encodedStr)
#converter formato para link final da url
#conv = urllib.parse.quote(encodedStr)
print(conv)

    
