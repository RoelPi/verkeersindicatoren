import json
import requests
import pandas as pd
import csv

pd.set_option('precision', 0)

meta = requests.get('http://indicatoren.verkeerscentrum.be/geoserver/VC2017/ows?service=WFS&version=1.0.0&request=GetFeature&typeName=VC2017:Simplified_Buffer_2560&maxFeatures=5000&outputFormat=application%2Fjson')
jsonMeta = json.loads(meta.text)

wegen = [[str(f['properties']['SG_ID']).replace('.0',''),f['properties']['Wegcategor'],f['properties']['SG_naam']] for f in jsonMeta['features']]
wegen = pd.DataFrame(wegen, columns = ['identifier','wegcategorie','naam'])

wegen = wegen[wegen.naam.str.contains('Wetteren tot Merelbeke|'
    'Merelbeke tot Wetteren|'
    'Ternat tot Parking|'
    'Groot-Bijgaarden tot Ternat|'
    'Destelbergen tot Beervelde|'
    'Beervelde tot Destelbergen|'
    'Wilrijk tot U|'
    'A. tot Wilrijk|'
    'Zwijndrecht tot Kruibeke|'
    'Kruibeke tot Zwijndrecht|'
    'Machelen tot Vilvoorde-Koningslo|'
    'Cargo tot Zemst', regex = True)]
wegen.identifier = wegen.identifier.astype(str)
wegen['stad'] = ['Gent','Gent','Brussel','Brussel','Gent','Gent','Antwerpen','Antwerpen','Antwerpen','Antwerpen','Brussel','Brussel']

wegen.to_csv('legende.csv', index = False, quoting = csv.QUOTE_ALL)


# Volume
pdData = []
timer = 0
for year in range(2010,2019):
    for month in range(1,12):
        data = requests.get('http://indicatoren.verkeerscentrum.be/vc.indicators.web.gui/verkeersvolumeIndicator/visualmapData?criteria={"ruimtelijke_aggregatie":"4","dagtype_id":"8","dagdeel_id":"1","voertuigklasse_id":"8","wegcategorie_groepid":"1","visualmapType":"month","month":' + str(month) + ',"year":' + str(year) + '}')
        jsonData = json.loads(data.text)
        pdData.append(pd.DataFrame(jsonData['dataList'], columns = ['identifier','voertuigen']))
        pdData[timer]['jaar'] = year
        pdData[timer]['maand'] = month
        timer = timer + 1

data = pd.concat(pdData)
data = data.sort_values(by = ['identifier','jaar','maand'])

data.identifier = data.identifier.astype(str)
data = data.merge(wegen, on = 'identifier')

data.to_csv('all_volume.csv', index = False, quoting = csv.QUOTE_ALL)

# Verzadiging
pdData = []
timer = 0
for year in range(2010,2019):
    for month in range(1,12):
        data = requests.get('http://indicatoren.verkeerscentrum.be/vc.indicators.web.gui/verzadigingsgraadIndicator/visualmapData?criteria={"ruimtelijke_aggregatie":"4","dagtype_id":"10","dagdeel_id":"1","voertuigklasse_id":"dummy","wegcategorie_groepid":"1","visualmapType":"month","month":' + str(month) + ',"year":' + str(year) + '}')
        jsonData = json.loads(data.text)
        pdData.append(pd.DataFrame(jsonData['dataList'], columns = ['identifier','verzadiging']))
        pdData[timer]['jaar'] = year
        pdData[timer]['maand'] = month
        timer = timer + 1

data = pd.concat(pdData)
data = data.sort_values(by = ['identifier','jaar','maand'])

data.identifier = data.identifier.astype(str)
data = data.merge(wegen, on = 'identifier')

data.to_csv('all_verzadiging.csv', index = False, quoting = csv.QUOTE_ALL)