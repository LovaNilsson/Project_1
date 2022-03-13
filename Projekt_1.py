#Test

import os
import urllib.request
import json
import discord

from datetime import datetime
from pytz import timezone
import pytz

def utc_time(dt):
    dt = dt.split (',')
    year = int(dt[0])
    month = int(dt[1])
    day = int(dt[2])
    hour = int(dt[3])
    dt = str(datetime(year, month, day, hour))
    
    local = pytz.timezone("Europe/Stockholm")
    naive = datetime.strptime(dt, "%Y-%m-%d %H:%M:%S")
    local_dt = local.localize(naive, is_dst=None)
    utc_dt = local_dt.astimezone(pytz.utc)

    utc_dt = str(utc_dt)
    utc_dt = utc_dt.replace(' ', 'T')
    utc_dt = utc_dt.replace('+00:00', 'Z')

    return utc_dt

def coordinates(plats, landsnummer):

    coordinatesUrl = "http://api.openweathermap.org/geo/1.0/direct?q="+plats+","+landsnummer+"&appid=1b584e5164c75e79f09b30ef48428487"
    
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
    tid_nr_d = tidsserie[d]["validTime"]
    validDate = tid_nr_d[0:10]
    validHour = tid_nr_d[11:13]
    date = datum_tid[0:10]
    hour = datum_tid[11:13]

    while validDate!=date:
        tid_nr_d = tidsserie[d]["validTime"]
        validDate = tid_nr_d[0:10]
        d+=1

    while validHour < hour:
        tid_nr_d = tidsserie[d]["validTime"]
        validHour = tid_nr_d[11:13]
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


def svar(prognos):
    väderlista = ['klar himmel', 'mestadels klar himmel', 'växlande molnighet', 'halvklart', 'molnigt', 'mulet', 'dimmigt', 'lätta regnskurar', 'regnigt', 'häftiga regnskurar', 'åskstorm', 'lätt snöblandat regn', 'snöblandat regn', 'mycket snöblandat regn','lätt snöfall', 'snöfall', 'mycket snö', 'lätt regn', 'regnigt', 'mycket regn', 'åska', 'lätt snöblandat regn', 'snöblandat regn', 'mycket snöblandat regn', 'lätt snöfall', 'snöfall', 'mycket snö']

    väder = väderlista[prognos[0][0]-1]
    temperatur = str(prognos[1][0])

    return "Det blir " + väder + " och " + temperatur.replace('.',',') + " °C."

def byt_ut_åäö(plats):
    #byt ut å, ä, ö om det finns i platsnamnet
    if "å" in plats:
        plats = plats.replace('å','a')
    elif "ä" in plats:
     plats = plats.replace('ä','a')
    elif "ö" in plats:
        plats = plats.replace('ö','a')
    return(plats)

client = discord.Client()

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))
 
@client.event
async def on_message(message):
    if message.author == client.user:
        return
 
    if message.content.startswith('Vädermannen!'):
        await message.channel.send('Hallå där!')

    if 'väder' in message.content:
        await message.channel.send('Väder är trevligt ja, vilken plats vill du ha en prognos för? Jag kan bara ge prognoser för platser i Sverige')
        
        def check(m):
            return m.content
        
        msg = await client.wait_for('message', check=check)
        plats = check(msg)
        plats = byt_ut_åäö(plats)

        await message.channel.send('Tyvärr finns endast prognoser för de närmaste 10 dygnen. Skriv in datum och tid på formen åååå, mm, dd, tt.')
        msg = await client.wait_for('message', check=check)
        tid = check(msg)
        tid = utc_time(tid)
        #Jag har inte fixat till så att tiden blir rätt än men själva boten fungerar nu! Jag vet dock inte vad som händer om man skriver in en plats som inte finns
        #Tiden ska funka nu

        landsnummer = "725"

        koordinater = coordinates(plats, landsnummer)
        lon = str("{0:0.0f}".format(koordinater[0]))
        lat = str("{0:0.0f}".format(koordinater[1]))

        prognos = forecast(lon, lat, tid)
       
        await message.channel.send(svar(prognos))





client.run('OTQwMjI2MjY0NTU4NjI0Nzc4.YgET8g.rsVaplQRu9GyAprVmoVVICkLUKs')