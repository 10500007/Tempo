"""
Módulo para recuperação de dados climáticos do PCBr.

    A documentação do Projeto pode ser encontrada no Portal
          http://pclima.inpe.br/
     
    As escolhas para o download de dados são definidas através 
     de um JSON que pode ser gerado utilizando do Portal API.
          http://pclima.inpe.br/analise/API
 
    versão do Python em que foi testada: 3.6
     
    exemplo de uso da API

    Token: consultar a documentação para a geração do Token

    Copiar o Token, no arquivo $HOME/.pclimaAPIrc (em ambiente Unix/Linux/Mac).
    Em Windows colocar o arquivo .pclimaAPIrc no diretório inicial do usuário (ex. C:\\User\\Cliente)


    import pclima as pcl

    Client = pcl.Client()

    data = Client.getData(
    { "formato": "CSV", "conjunto": "PR0002", "modelo": "MO0003", "experimento": "EX0003", "periodo": "PE0000", "cenario": "CE0001", "variavel": "VR0001", "frequenciaURL": "Mensal", "frequencia": "FR0003", "produto": "PDT0001", "localizacao": "Ponto", "localizacao_pontos": "-23.56/-46.62", "varCDO": "tasmax" }
    )

    Client.save(data,"file.csv") 
     
"""

__all__ = ['Client']

from .api import *

