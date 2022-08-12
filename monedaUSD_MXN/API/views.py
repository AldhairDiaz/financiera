from django.shortcuts import render
from django.http import HttpResponse
import requests
from bs4 import BeautifulSoup
import re
from .models import CambioMoneda

def index(request):
    footer="Creado con DJANGO"
    context={
        'footer':footer
    }
    return render(request, 'API/index.html',context) 

def getDataScrapBanxico():
    url='https://www.banxico.org.mx/tipcamb/tipCamMIAction.do'
    req=requests.get(url)
    statusCode=req.status_code
    htmlText=req.text
    nombreCabeceras=[]
    dictBanxico={}
    
    if statusCode==200:
        html=BeautifulSoup(htmlText,"html.parser") 
        
        """ LISTA => Obtencion de nombre de cabeceras"""
        
        cabeceras=html.find_all('tr',{'class':'renglonTituloColumnas'})
        for cabecera in cabeceras:
            cabecera=cabecera.find_all('td')
            for name in cabecera:
                name=name.get_text()
                new_name=re.sub(r"[^a-zA-Z]","",name)
                
                nombreCabeceras.append(new_name)
        
        
        """ LISTA => Obtencion de datos """ 
        
        datos=html.find('tr',{'class':'renglonNon'})
        datos=datos.get_text().split()    
        
        
        """ Creacion de diccionario"""
        
        dictBanxico=dict(zip(nombreCabeceras,datos))
    context={
        'ScrapBanxico':dictBanxico
    }
    
    return context
        
def getDataAPIBanxico():
    idSerie='SF63528'
    fechaIni='2022-02-20'
    fechaFin='2022-02-27'
    dictAPIBanxico=''   
    
    token= '6d2007e254f59df59a3f80643bf1157560468f9143e9fb9f5a89c7d21fc9a073'
    header={
        'Bmx-Token':token
    }
    
    url=f'https://www.banxico.org.mx/SieAPIRest/service/v1/series/{idSerie}/datos/{fechaIni}/{fechaFin}'
    
    response=requests.get(url=url,headers=header)
    response=response.json()
    for dato in response['bmx']['series'][0]['datos']:
        dictAPIBanxico=dato
    
    context={
        'API_Banxico':dictAPIBanxico
    }
    return context
    
def getDataAPIFixer():
    
    access_key='d9466f56c44e2645ec9e6d86874d4dd5'
    symbols='MXN'
    url=f'http://data.fixer.io/api/latest?access_key={access_key}&symbols={symbols}'
    respuesta=requests.get(url=url)
    datos=respuesta.json()
    fecha=datos['date']
    mxn=str(datos['rates']['MXN'])
    dictFixer={'Fecha':fecha,'valor':mxn}
    context={
        'API_FIXER':dictFixer
    }
    return context    



def cargaBD():
    model=CambioMoneda
    dataSB = getDataScrapBanxico()['ScrapBanxico']
    fecha=dataSB['Fecha']
    valor=dataSB['Parapagos']
    
    
    dataAB=getDataAPIBanxico()['API_Banxico']
    fechaAB=dataAB['fecha']
    valorAB=dataAB['dato']
    
    
    dataAP=getDataAPIFixer()['API_FIXER']
    fechaAP=dataAP['Fecha']
    valorAP=dataAP['valor']
    
    
def getdictScrapAPIs(request):
    bd=cargaBD()
    bd.save()
    context={
        'bd':bd
    }
    return render(request,'API/apiView.html',context)
