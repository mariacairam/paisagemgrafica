#!/usr/bin/env python
# coding: utf-8

# In[2]:


import os
# import zipfile2
from PIL import Image
from PIL.ExifTags import TAGS
from PIL.ExifTags import GPSTAGS
import requests
import folium
from folium.features import CustomIcon
from iptcinfo3 import IPTCInfo
import numpy as np


# In[2]:


from urllib.request import urlopen
import urllib.request as request
from bs4 import BeautifulSoup
import io

import ssl
context = ssl._create_unverified_context()


br_site = "https://paisagemgrafica.joytill.com.br/fotos/BASES/"
req = request.Request(br_site,
                        headers={'User-Agent': 'Mozilla'})
http = request.urlopen(req, context=context)
soup = BeautifulSoup(http, 'html.parser')

pastas = []
for im in soup.findAll('a'):
    pastas.append(im.get('href'))

print(pastas)


# In[11]:


print('pasta: ' + pastas[15])
novoSite = br_site + pastas[15]
req = request.Request(novoSite,
                    headers={'User-Agent': 'Mozilla'})
http = request.urlopen(req, context=context)
soup = BeautifulSoup(http, 'html.parser')

arquivosPorPasta = []
for im in soup.findAll('a'):
    arquivosPorPasta.append(im.get('href'))

arquivosPorPasta.pop(0) 
arquivosPorPasta.pop(0) 
arquivosPorPasta.pop(0) 
arquivosPorPasta.pop(0) 
arquivosPorPasta.pop(0)
#print(arquivosPorPasta)


tituloImagem = []
keywords = []
data = []
coordenada = []

print('quantidade de imagens: ' + str(len(arquivosPorPasta)))
m = 1

for j in arquivosPorPasta:
    testandoTipo = j.split('.')

    if (testandoTipo[len(testandoTipo)-1] != 'jpg' and testandoTipo[len(testandoTipo)-1] != 'JPG' 
    and testandoTipo[len(testandoTipo)-1] != 'png'):
        print (testandoTipo[len(testandoTipo)-1])
        print('arquivo de vídeo')
        continue
    # print(j)
    # print(m)
    newreq = request.Request(novoSite + j,
                        headers={'User-Agent': 'Chrome'})
    abriraurlNova = request.urlopen(newreq, context=context)
    try:
        arquivoImagem = io.BytesIO(abriraurlNova.read())
        img = Image.open(arquivoImagem)
    except Exception as e:
        print('erro de imagem')
        continue
    #info = IPTCInfo(arq_img)
  #  print (info['keywords'])
    #for word in info['keywords']:
     #   keywords.append(word)
    try:
        exifdata = img.getexif()
        for tagid in exifdata:
            tagname = TAGS.get(tagid, tagid)
            value = exifdata.get(tagid)

        exif = {}
        for tag, value in img._getexif().items():
            if tag in TAGS:
                exif[TAGS[tag]] = value
    except AttributeError:
        print('sem dados')
        pass

#tentar obter de uma maneira única    
    try:
        datatempo=exif['DateTime']

        gps_info={}
        for k, v in exif['GPSInfo'].items():
            geo_tag=GPSTAGS.get(k)
            gps_info[geo_tag]=v

    #print(gps_info)

        lat=gps_info['GPSLatitude']
        long=gps_info['GPSLongitude']


    #print(lat)
    #print(long)

#verificar conversão
        lat=float(lat[0]+(lat[1]/60)+(lat[2]/(3600)))
        long=float(long[0]+(long[1]/60)+(long[2]/(3600)))

        if gps_info['GPSLatitudeRef']=='S':
            lat=-lat
        if gps_info['GPSLongitudeRef']=='W':
            long=-long
        coordenada.append([lat, long])
        data.append(datatempo)
        tituloImagem.append(j)
    except KeyError:
        print('sem algum dado')
    m += 1


# In[ ]:


ano2016 = open("2016.txt", 'w')
print(len(tituloImagem), len(coordenada), len(data))
for index in range(0, len(tituloImagem), 1):
    ano2016.write(novoSite + ',' + tituloImagem[index] + ',' + str(coordenada[index][0]) + ',' + 
                  str(coordenada[index][1]) + ',' + data[index] + '\n')


# In[5]:


ano2016.close()


# In[3]:


ano2013 = open("2013.txt", 'r')
infos1 = ano2013.readlines()

ano2014 = open("2014.txt", 'r')
infos2 = ano2014.readlines()

ano2015 = open("2015.txt", 'r')
infos3 = ano2015.readlines()

ano2016 = open("2016.txt", 'r')
infos3 = ano2016.readlines()

ano2017 = open("2017.txt", 'r')
infos5 = ano2017.readlines()

ano2018 = open("2018.txt", 'r')
infos6 = ano2018.readlines()

ano2019 = open("2019.txt", 'r')
infos7 = ano2019.readlines()

ano2020 = open("2020.txt", 'r')
infos8 = ano2020.readlines()

ano2021 = open("2021.txt", 'r')
infos9 = ano2021.readlines()

ano2022 = open("2022.txt", 'r')
infos10 = ano2022.readlines()

infos = infos1+infos2+infos3+infos5+infos6+infos7+infos8+infos9+infos10

cl = {'2013': 'gray', '2014': 'red', '2015': 'lightblue', '2016': 'darkgreen', '2017': 'orange', '2018': 'green', '2019': 'purple', '2020': 'blue', '2021': 'pink', '2022': 'black'}
m=folium.Map(location=[lat,long],zoom_start=12) 
j = 0
tooltip = "Click me!"
for information in infos:
    cadaRegistro = information.split(',')
    dataHora = cadaRegistro[4].split(':')
    dia = dataHora[2].split(' ')
    data = dia[0] + '/' + dataHora[1] + '/' + dataHora[0]
    link = '<a href='+ cadaRegistro[0] + cadaRegistro[1] +  '>Link para imagem</a>'
    popup = data + '\n' + link
#folium.CircleMarker(location=[lat,long],fill=True, color='red',fill_color='red').add_to(m)
    marker = folium.Marker(location=[cadaRegistro[2], cadaRegistro[3]], popup=popup, tooltip=tooltip, 
                                     icon=folium.Icon(color=cl[dataHora[0]], icon='picture'))
    marker.add_to(m)
m.save('map_completo.html')
m
# In[ ]:


from folium.plugins import MarkerCluster
cl = {'2013': 'gray', '2014': 'red', '2015': 'lightblue', '2016': 'darkgreen', '2017': 'orange', '2018': 'green', '2019': 'purple', '2020': 'blue', '2021': 'pink', '2022': 'black'}
m=folium.Map(location=[-22.983619444444443,-43.20545277777778],zoom_start=12) 
marker_cluster = MarkerCluster(disableClusteringAtZoom=18, spyderfyOnMaxZoom=False).add_to(m)
j = 0
tooltip = "Click me!"
for information in infos:
    cadaRegistro = information.split(',')
    dataHora = cadaRegistro[4].split(':')
    dia = dataHora[2].split(' ')
    data = dia[0] + '/' + dataHora[1] + '/' + dataHora[0]
    link = '<a href='+ cadaRegistro[0] + cadaRegistro[1] +  '>Link para imagem</a>'
    popup = data + '\n' + link
#folium.CircleMarker(location=[lat,long],fill=True, color='red',fill_color='red').add_to(m)
    marker = folium.Marker(location=[cadaRegistro[2], cadaRegistro[3]], popup=popup, tooltip=tooltip, 
                                     icon=folium.Icon(color=cl[dataHora[0]], icon='picture')).add_to(marker_cluster)
m.save('map_completo_cluster_2.html')
m


# In[6]:


from folium.plugins import MarkerCluster
cl = {'2013': 'gray', '2014': 'red', '2015': 'lightblue', '2016': 'darkgreen', '2017': 'orange', '2018': 'green', '2019': 'purple', '2020': 'blue', '2021': 'pink', '2022': 'black'}
m=folium.Map(location=[-22.983619444444443,-43.20545277777778],zoom_start=12)

f_geral = folium.FeatureGroup(name='todas as imagens', show=True).add_to(m)

f_2013 = folium.FeatureGroup(name='2013 (cinza)', show=False).add_to(m)
f_2014 = folium.FeatureGroup(name='2014 (vermelho)', show=False).add_to(m)
f_2015 = folium.FeatureGroup(name='2015 (azul claro)', show=False).add_to(m)
f_2016 = folium.FeatureGroup(name='2016 (verde escuro)', show=False).add_to(m)
f_2017 = folium.FeatureGroup(name='2017 (laranja)', show=False).add_to(m)
f_2018 = folium.FeatureGroup(name='2018 (verde)', show=False).add_to(m)
f_2019 = folium.FeatureGroup(name='2019 (roxo)', show=False).add_to(m)
f_2020 = folium.FeatureGroup(name='2020 (azul)', show=False).add_to(m)
f_2021 = folium.FeatureGroup(name='2021 (rosa)', show=False).add_to(m)
f_2022 = folium.FeatureGroup(name='2022 (preto)', show=False).add_to(m)



marker_cluster = MarkerCluster().add_to(f_geral)

marker_cluster_2013 = MarkerCluster(disableClusteringAtZoom=18, spyderfyOnMaxZoom=False).add_to(f_2013)
marker_cluster_2014 = MarkerCluster(disableClusteringAtZoom=18, spyderfyOnMaxZoom=False).add_to(f_2014)
marker_cluster_2015 = MarkerCluster(disableClusteringAtZoom=18, spyderfyOnMaxZoom=False).add_to(f_2015)
marker_cluster_2016 = MarkerCluster(disableClusteringAtZoom=18, spyderfyOnMaxZoom=False).add_to(f_2016)
marker_cluster_2017 = MarkerCluster(disableClusteringAtZoom=18, spyderfyOnMaxZoom=False).add_to(f_2017)
marker_cluster_2018 = MarkerCluster(disableClusteringAtZoom=18, spyderfyOnMaxZoom=False).add_to(f_2018)
marker_cluster_2019 = MarkerCluster(disableClusteringAtZoom=18, spyderfyOnMaxZoom=False).add_to(f_2019)
marker_cluster_2020 = MarkerCluster(disableClusteringAtZoom=18, spyderfyOnMaxZoom=False).add_to(f_2020)
marker_cluster_2021 = MarkerCluster(disableClusteringAtZoom=18, spyderfyOnMaxZoom=False).add_to(f_2021)
marker_cluster_2022 = MarkerCluster(disableClusteringAtZoom=18, spyderfyOnMaxZoom=False).add_to(f_2022)


j = 0
tooltip = "Click me!"
for information in infos:
    cadaRegistro = information.split(',')
    dataHora = cadaRegistro[4].split(':')
    dia = dataHora[2].split(' ')
    data = dia[0] + '/' + dataHora[1] + '/' + dataHora[0]
    link = '<a href='+ cadaRegistro[0] + cadaRegistro[1] +  '>Link para imagem</a>'
    popup = data + '\n' + link

    if (dataHora[0] == '2013'):
        marker0 = folium.Marker(location=[cadaRegistro[2], cadaRegistro[3]], popup=popup, tooltip=tooltip, 
                                     icon=folium.Icon(color=cl[dataHora[0]], icon='picture')).add_to(marker_cluster)
        marker = folium.Marker(location=[cadaRegistro[2], cadaRegistro[3]], popup=popup, tooltip=tooltip, 
                                     icon=folium.Icon(color=cl[dataHora[0]], icon='picture')).add_to(marker_cluster_2013)
    elif (dataHora[0] == '2014'):
        marker0 = folium.Marker(location=[cadaRegistro[2], cadaRegistro[3]], popup=popup, tooltip=tooltip, 
                                     icon=folium.Icon(color=cl[dataHora[0]], icon='picture')).add_to(marker_cluster)
        marker = folium.Marker(location=[cadaRegistro[2], cadaRegistro[3]], popup=popup, tooltip=tooltip, 
                                     icon=folium.Icon(color=cl[dataHora[0]], icon='picture')).add_to(marker_cluster_2014)
    elif (dataHora[0] == '2015'):
        marker0 = folium.Marker(location=[cadaRegistro[2], cadaRegistro[3]], popup=popup, tooltip=tooltip, 
                                     icon=folium.Icon(color=cl[dataHora[0]], icon='picture')).add_to(marker_cluster)
        marker = folium.Marker(location=[cadaRegistro[2], cadaRegistro[3]], popup=popup, tooltip=tooltip, 
                                     icon=folium.Icon(color=cl[dataHora[0]], icon='picture')).add_to(marker_cluster_2015)
    elif (dataHora[0] == '2016'):
        marker0 = folium.Marker(location=[cadaRegistro[2], cadaRegistro[3]], popup=popup, tooltip=tooltip, 
                                     icon=folium.Icon(color=cl[dataHora[0]], icon='picture')).add_to(marker_cluster)
        marker = folium.Marker(location=[cadaRegistro[2], cadaRegistro[3]], popup=popup, tooltip=tooltip, 
                                     icon=folium.Icon(color=cl[dataHora[0]], icon='picture')).add_to(marker_cluster_2016)
    elif (dataHora[0] == '2017'):
        marker0 = folium.Marker(location=[cadaRegistro[2], cadaRegistro[3]], popup=popup, tooltip=tooltip, 
                                     icon=folium.Icon(color=cl[dataHora[0]], icon='picture')).add_to(marker_cluster)
        marker = folium.Marker(location=[cadaRegistro[2], cadaRegistro[3]], popup=popup, tooltip=tooltip, 
                                     icon=folium.Icon(color=cl[dataHora[0]], icon='picture')).add_to(marker_cluster_2017)
    elif (dataHora[0] == '2018'):
        marker0 = folium.Marker(location=[cadaRegistro[2], cadaRegistro[3]], popup=popup, tooltip=tooltip, 
                                     icon=folium.Icon(color=cl[dataHora[0]], icon='picture')).add_to(marker_cluster)
        marker = folium.Marker(location=[cadaRegistro[2], cadaRegistro[3]], popup=popup, tooltip=tooltip, 
                                     icon=folium.Icon(color=cl[dataHora[0]], icon='picture')).add_to(marker_cluster_2018)
    elif (dataHora[0] == '2019'):
        marker0 = folium.Marker(location=[cadaRegistro[2], cadaRegistro[3]], popup=popup, tooltip=tooltip, 
                                     icon=folium.Icon(color=cl[dataHora[0]], icon='picture')).add_to(marker_cluster)
        marker = folium.Marker(location=[cadaRegistro[2], cadaRegistro[3]], popup=popup, tooltip=tooltip, 
                                     icon=folium.Icon(color=cl[dataHora[0]], icon='picture')).add_to(marker_cluster_2019)
    elif (dataHora[0] == '2020'):
        marker0 = folium.Marker(location=[cadaRegistro[2], cadaRegistro[3]], popup=popup, tooltip=tooltip, 
                                     icon=folium.Icon(color=cl[dataHora[0]], icon='picture')).add_to(marker_cluster)
        marker = folium.Marker(location=[cadaRegistro[2], cadaRegistro[3]], popup=popup, tooltip=tooltip, 
                                     icon=folium.Icon(color=cl[dataHora[0]], icon='picture')).add_to(marker_cluster_2020)
    elif (dataHora[0] == '2021'):
        marker0 = folium.Marker(location=[cadaRegistro[2], cadaRegistro[3]], popup=popup, tooltip=tooltip, 
                                     icon=folium.Icon(color=cl[dataHora[0]], icon='picture')).add_to(marker_cluster)
        marker = folium.Marker(location=[cadaRegistro[2], cadaRegistro[3]], popup=popup, tooltip=tooltip, 
                                     icon=folium.Icon(color=cl[dataHora[0]], icon='picture')).add_to(marker_cluster_2021)
    elif (dataHora[0] == '2022'):
        marker0 = folium.Marker(location=[cadaRegistro[2], cadaRegistro[3]], popup=popup, tooltip=tooltip, 
                                     icon=folium.Icon(color=cl[dataHora[0]], icon='picture')).add_to(marker_cluster)
        marker = folium.Marker(location=[cadaRegistro[2], cadaRegistro[3]], popup=popup, tooltip=tooltip, 
                                     icon=folium.Icon(color=cl[dataHora[0]], icon='picture')).add_to(marker_cluster_2022)
        

folium.LayerControl(collapsed=False).add_to(m)

m.save('map_completo_cluster_layers.html')
m

