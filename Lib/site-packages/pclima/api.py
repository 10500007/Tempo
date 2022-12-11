import os
import json
from pclima.factory import RequestFactory

class Client(object):
    """
    Classe utilizada para criar um Cliente de acesso a API.

    Attributes
    ----------
    token : str
        Definido no arquivo ~/.pclimaAPIrc
    format : str
        Formato do download, definido no getData


    """
    def __init__(self, token=os.environ.get("API_TOKEN"),):
        """
        Parameters
        ----------
        token : str
            Chave de acesso aos serviços da API

        """
        self.token = token
        self.format = None

        if (os.name == 'nt'): 
            pontorc = os.environ.get("PCLIMAAPI_RC", os.path.expanduser("~\\.pclimaAPIrc"))
        else:
            pontorc = os.environ.get("PCLIMAAPI_RC", os.path.expanduser("~/.pclimaAPIrc"))



        if token is None:
            if os.path.exists(pontorc):
                config = read_config(pontorc)

                if token is None:
                    token = config.get("token")

        if token is None:
            print("Missing/incomplete configuration file: %s" % (pontorc))
            raise SystemExit
            
        self.token = token


    def getData(self,apiJSON):
        """
        Method
        -------
        O Método envia o JSON e retorna os dados desejados.  

        Parameters
        ----------
        apiJSON : json
            JSON com as opções escolhidas

        Returns
        -------
        retorno depende do formato escolhido:
        
        Formato             Retorno:
        NetCDF              XArray
        CSV                 DataFrame
        JSON                DataFrame
        CSVPontos           DataFrame
        CSVPontosTransposta DataFrame 
        """
       
        j = json.loads(json.dumps(apiJSON))

        self.format = j["formato"]

        factory = RequestFactory()
        product = factory.get_order(j["formato"],self.token,j)
        return (product.download())

    def save(self,content,file):
        """
        Method
        -------
        O Método decebe a recuperacao do dado e o nome do arquivo
        se saída.

        Parameters
        ----------
        content : formato desejado
            Dados recuperados

        file : nome do arquivo de saída
            Nome do arquivo de saída Ex.: "saida.csv"
        """
        factory = RequestFactory()
        factory.save(self.format,content,file)

def read_config(path):
    config = {}
    with open(path) as f:
        for l in f.readlines():
            if ":" in l:
                k, v = l.strip().split(":", 1)
                if k in ("token"):
                    config[k] = v.strip()
    return config
