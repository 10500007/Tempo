from abc import ABC, abstractmethod
from pclima.http_util import PClimaURL
import json
import pandas as pd
import requests
import io
import xarray as xr
import numpy as np

class RequestFactory:
    def get_order(self, type_of_order,token,json):
        if type_of_order == "NetCDF":
            return Netcdf(token, json)
        if type_of_order == "CSV":
            return Csv(token, json)
        if type_of_order == "CSVPontos":
            return CSVPontos(token, json)            
        if type_of_order == "CSVPontosT":
            return CSVPontosT(token, json)  
        if type_of_order == "JSON":
            return JSON(token, json)

    def save(self, type_of_order,content,file):
        if type_of_order == "NetCDF":
            saveNetcdf(content,file)
        if type_of_order == "CSV":
            saveCSV(content,file)
        if type_of_order == "CSVPontos":
            saveCSV(content,file)
        if type_of_order == "CSVPontosT":
            saveCSV(content,file)
        if type_of_order == "JSON":
            saveJSON(content,file)

class Product(ABC):

    @abstractmethod
    def download(self):
        pass

class Netcdf(Product):
    def __init__(self, token, json):
        self.token = token
        self.json = json

    def download(self):
        c1 = PClimaURL()
        url = c1.get_url(self.json)
        (anoInicial,anoFinal)=verificaIntervaloAnos(self.json)

        if (anoInicial and anoFinal):
            return (download_toNetCDFInterval(url, self.token,anoInicial,anoFinal))
        else:
            return (download_toNetCDF(url, self.token))

    def __str__(self):
        return self.token+" ["+str(self.json)+"] "


class Csv(Product):
    def __init__(self, token, json):
        self.token = token
        self.json = json

    def download(self):
        c1 = PClimaURL()
        url = c1.get_url(self.json)
        (anoInicial,anoFinal)=verificaIntervaloAnos(self.json)

        if (anoInicial and anoFinal):
            return (download_toCSVInterval(url, self.token,anoInicial,anoFinal))
        else:
            return (download_toCSV(url, self.token))

class JSON(Product):
    def __init__(self, token, json):
        self.token = token
        self.json = json

    def download(self):
        c1 = PClimaURL()
        url = c1.get_url(self.json)
        (anoInicial,anoFinal)=verificaIntervaloAnos(self.json)

        if (anoInicial and anoFinal):
            return (download_toCSVInterval(url, self.token,anoInicial,anoFinal))
        else:            
            return (download_toJSON(url, self.token))

class CSVPontos(Product):
    def __init__(self, token, json):
        self.token = token
        self.json = json

    def download(self):
        c1 = PClimaURL()
        url = c1.get_url(self.json)
        (anoInicial,anoFinal)=verificaIntervaloAnos(self.json)
        (mesInicial,mesFinal)=verificaIntervaloMes(self.json)

        if (mesInicial and mesFinal):
            if (anoInicial and anoFinal):
                return (download_toCSVPontosAnoMesInterval(url, self.token,anoInicial,anoFinal,mesInicial,mesFinal))
            else:  
                return (download_toCSVPontosMesInterval(url, self.token,anoInicial,mesInicial,mesFinal))
        elif (mesInicial): 
            return (download_toCSVPontos(url, self.token))
        elif (anoInicial and anoFinal):
            return (download_toCSVPontosAnoInterval(url, self.token,anoInicial,anoFinal))
        else:  
             return (download_toCSVPontos(url, self.token))

class CSVPontosT(Product):
    def __init__(self, token, json):
        self.token = token
        self.json = json

    def download(self):
        c1 = PClimaURL()
        url = c1.get_url(self.json)
        (anoInicial,anoFinal)=verificaIntervaloAnos(self.json)
        (mesInicial,mesFinal)=verificaIntervaloMes(self.json)

        if (mesInicial and mesFinal):
            if (anoInicial and anoFinal):
                return (download_toCSVPontosTAnoMesInterval(url, self.token,anoInicial,anoFinal,mesInicial,mesFinal))
            else:
                return (download_toCSVPontosTMesInterval(url, self.token,anoInicial,mesInicial,mesFinal))
        elif (mesInicial): 
            return (download_toCSVPontosT(url, self.token))
        if (anoInicial and anoFinal):
            return (download_toCSVPontosTAnoInterval(url, self.token,anoInicial,anoFinal))
        else:        
            return (download_toCSVPontosT(url, self.token))

    def __str__(self):   
        return self.token+" ["+str(self.json)+"]"

def download_toCSV( url, token):
    r=downloadData(url, token)
    rawData = pd.read_csv(io.StringIO(r.content.decode('utf-8')))
    return rawData

def download_toJSON( url, token):
    r=downloadData(url, token)
    rawData = pd.read_json(io.StringIO(r.content.decode('utf-8')))
    return rawData

def download_toCSVPontos( url, token):
    r=downloadData(url, token)
    rawData = pd.read_csv(io.StringIO(r.content.decode('utf-8')))
    return rawData

def download_toCSVPontosT( url, token):
    r=downloadData(url, token)
    rawData = pd.read_csv(io.StringIO(r.content.decode('utf-8')))
    return rawData

def download_toNetCDF(url, token):
    r=downloadData(url, token)
    return xr.open_dataset(r.content)

def saveNetcdf(content,file):
	content.to_netcdf(file)

def saveCSV(content,file):
	content.to_csv(file)

def saveJSON(content,file):
	content.to_json(file,date_format='iso')

def downloadData(url, token):
    headers = { 'Authorization' : 'Token ' + token }
    r = requests.get(url, headers=headers, verify=False)
    if (r.status_code != requests.codes.ok):
        msg=""
        if (r.status_code == 401):
            msg="Favor verificar seu Token"
        elif (r.status_code == 404):
            msg="Arquivo ou URL não encontrado. Favor verificar JSON de entrada"
        else:
            msg=r.reason
        print (msg)
        raise SystemExit
    return r

def verificaIntervaloAnos(json):
    anoInicial=""
    anoFinal=""
    try:
        (anoInicial, anoFinal) = json["ano"].split("-")
    except:
        pass
    return (anoInicial, anoFinal)

def verificaIntervaloMes(json):
    mesInicial=""
    mesFinal=""
    try:
        (mesInicial, mesFinal) = json["mes"].split("-")
    except:
        try:
            mesInicial=json["mes"]
        except:
            mesInicial=""
            pass
    return (mesInicial, mesFinal)

def download_toNetCDFInterval(url,token,anoInicial,anoFinal):
    mergedAno=0
    ds=download_toNetCDF(url[:-9]+str(anoInicial), token)
    for ano in range(int(anoInicial)+1, int(anoFinal)+1): 
        ds1=download_toNetCDF(url[:-9]+str(ano), token)
        if (mergedAno==0):

            dsmerged = xr.merge([ds,ds1])
        else:
            dsmerged = xr.merge([dsmerged,ds1])
                
        mergedAno=1
        if (ano==int(anoFinal)):
            return (dsmerged)

def download_toCSVInterval(url,token,anoInicial,anoFinal):
    df = pd.DataFrame()
    for ano in range(int(anoInicial), int(anoFinal)+1):
        df1=(download_toCSV(url[:-9]+str(ano), token))
        frames = [df, df1]
        df = pd.concat(frames)
    df.reset_index(drop=True, inplace=True)
    return (df)

def download_toJSONInterval(url,token,anoInicial,anoFinal):
    df = pd.DataFrame()
    for ano in range(int(anoInicial), int(anoFinal)+1):
        df1=(download_toJSON(url[:-9]+str(ano), self.token))
        frames = [df, df1]
        df = pd.concat(frames)
    return (df)

def download_toCSVPontosAnoInterval(url,token,anoInicial,anoFinal):
    df = pd.DataFrame()
    for ano in range(int(anoInicial), int(anoFinal)+1):
        df1=(download_toCSVPontos(url[:-9]+str(ano), token))
        frames = [df, df1]
        df = pd.concat(frames, axis=1)
    return (df)

def download_toCSVPontosMesInterval(url,token,anoInicial,mesInicial,mesFinal):
    df = pd.DataFrame()
    for mes in range(int(mesInicial), int(mesFinal)+1):
        df1=(download_toCSVPontos(url[:-5]+str(mes), token))
        frames = [df, df1]
        df = pd.concat(frames, axis=1)
    return (df)

def download_toCSVPontosAnoMesInterval(url,token,anoInicial,anoFinal,mesInicial,mesFinal):
    df = pd.DataFrame()
    for ano in range(int(anoInicial), int(anoFinal)+1):
        for mes in range(int(mesInicial), int(mesFinal)+1):
            urlAno=url[:-15]+str(ano)
            df1=(download_toCSVPontos(urlAno+"/"+str(mes), token))
            frames = [df, df1]
            df = pd.concat(frames, axis=1)
    return (df)

def download_toCSVPontosTAnoInterval(url,token,anoInicial,anoFinal):
    df = pd.DataFrame()
    for ano in range(int(anoInicial), int(anoFinal)+1):
        df1=(download_toCSVPontos(url[:-9]+str(ano), token))
        if (ano != int(anoInicial)): 
        	df1 = df1[2:]
        frames = [df, df1]
        df = pd.concat(frames)
    df.reset_index(drop=True, inplace=True)
    return (df)

def download_toCSVPontosTMesInterval(url,token,anoInicial,mesInicial,mesFinal):
    df = pd.DataFrame()
    for mes in range(int(mesInicial), int(mesFinal)+1):
        df1=(download_toCSVPontos(url[:-5]+str(mes), token))
        if (mes != int(mesInicial)): 
            df1 = df1[2:]
        frames = [df, df1]
        df = pd.concat(frames)
    df.reset_index(drop=True, inplace=True)
    return (df)

def download_toCSVPontosTAnoMesInterval(url,token,anoInicial,anoFinal,mesInicial,mesFinal):
    df = pd.DataFrame()
    for ano in range(int(anoInicial), int(anoFinal)+1):    
        for mes in range(int(mesInicial), int(mesFinal)+1):
            urlAno=url[:-15]+str(ano)
            df1=(download_toCSVPontosT(urlAno+"/"+str(mes), token))
            if (mes != int(mesInicial) or ano != int(anoInicial) ): 
                df1 = df1[2:]
            frames = [df, df1]
            df = pd.concat(frames)
    df.reset_index(drop=True, inplace=True)
    return (df)
