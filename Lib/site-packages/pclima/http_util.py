#import requests
import posixpath


class HTTPEndPoint(object):
    def __init__(self):
        #self._base = 'http://0.0.0.0:8888/api/v1/public/'
        self._base = 'http://4cn-api.cptec.inpe.br/api/v1/public/'

class PClimaURL(HTTPEndPoint):

    def get_url(self, json):
        path = ('{t1}/'
                '{t2}/{t3}/{t4}'
                '/{t6}/{t7}/{t8}/{t5}/{t9}/{t10}/{t11}/{t12}/{t13}{t14}{t15}{t16}{t17}{t18}').format(t1=json["localizacao"], t2=json["formato"],
                t3=json["frequenciaURL"], t4=json["localizacao_pontos"],
                t6=json["conjunto"],t7=json["modelo"], t8=json["experimento"],t5=json["periodo"],t9=json["cenario"],
                t10=json["variavel"],t11=json["frequencia"], t12=json["produto"],t13=json["varCDO"],
                t14="/"+json["ano"] if json["frequencia"] == "FR0004" else "",
                t15="/"+json["ano"] if json["frequencia"] == "FR0003" and json["formato"] =="CSVPontos" else "",
                t16="/"+json["ano"] if json["frequencia"] == "FR0003" and json["formato"] =="CSVPontosT" else "",
                t17="/"+json["mes"] if json["frequencia"] == "FR0004" and json["formato"] =="CSVPontos" else "",
                t18="/"+json["mes"] if json["frequencia"] == "FR0004" and json["formato"] =="CSVPontosT" else "")

        return (self.url_path(path))

    def url_path(self, path):
        return posixpath.join(self._base, path) 


