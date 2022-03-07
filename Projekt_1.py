#Test

import os
import urllib.request
import json


text = ""

def time(text):
    print("HEJ")



def coordinates(stad, landsnummer):

    coordinatesUrl = "http://api.openweathermap.org/geo/1.0/direct?q="+stad+","+landsnummer+"&appid=1b584e5164c75e79f09b30ef48428487"
    
    a = urllib.request.urlopen(coordinatesUrl) 
    b = a.read()
    c = json.loads(b)
    lon = c[0]["lon"]
    lat = c[0]["lat"]
    
    return(lon, lat)


def forecast(longitud, latitud, datum_tid):

    lon = longitud
    lat = latitud
    forecastUrl = 'https://opendata-download-metfcst.smhi.se/api/category/pmp3g/version/2/geotype/point/lon/'+lon+'/lat/'+lat+'/data.json'
    
    a = urllib.request.urlopen(forecastUrl) 
    b = a.read()
    c = json.loads(b)
    tidsserie = c["timeSeries"]
    
    #Hitta rätt tid och datum
    d = 0
    tid = datum_tid
    while tidsserie[d]["validTime"]!=tid:
        d+=1
    
    #Hitta temperatur
    e = 0
    while tidsserie[d]["parameters"][e]["name"]!="t":
        e+=1
    temperatur = tidsserie[d]["parameters"][e]["values"]

    #Hitta väder
    f = 0
    while tidsserie[d]["parameters"][f]["name"]!="Wsymb2":
        f+=1
    väder = tidsserie[d]["parameters"][f]["values"]
    
    return väder, temperatur



tid = "2022-03-08T14:00:00Z"
stad = "Sundsvall"
landsnummer = "725"

koordinater = coordinates(stad, landsnummer)
lon = str("{0:0.0f}".format(koordinater[0]))
lat = str("{0:0.0f}".format(koordinater[1]))

prognos = forecast(lon, lat, tid)

väderlista = ['klar himmel', 'mestadels klar himmel', 'växlande molnighet', 'halvklart', 'molnigt', 'mulet', 'dimmigt', 'lätta regnskurar', 'regnigt', 'häftiga regnskurar', 'åskstorm', 'lätt snöblandat regn', 'snöblandat regn', 'mycket snöblandat regn','lätt snöfall', 'snöfall', 'mycket snö', 'lätt regn', 'regnigt', 'mycket regn', 'åska', 'lätt snöblandat regn', 'snöblandat regn', 'mycket snöblandat regn', 'lätt snöfall', 'snöfall', 'mycket snö']

väder = väderlista[prognos[0][0]-1]
temperatur = str(prognos[1][0])

svar = "Det blir " + väder + " och " + temperatur.replace('.',',') + " °C."
print(svar)


#git config --global user.email "lova.nilsson@student.tabyenskilda.se"
#git config --global user.name "Lova"
