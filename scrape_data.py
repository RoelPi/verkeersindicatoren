import json
import requests
import pandas as pd

meta = requests.get('http://indicatoren.verkeerscentrum.be/geoserver/VC2017/ows?service=WFS&version=1.0.0&request=GetFeature&typeName=VC2017:Simplified_Buffer_2560&maxFeatures=5000&outputFormat=application%2Fjson')
jsonMeta = json.loads(meta.text)
print()
wegen = []
for f in jsonMeta:
    wegen.append([f['features'][1]['properties']['OBJECTID'],f['features'][1]['properties']['Wegcategor'],f['features'][1]['properties']['SG_naam']])


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
data.to_csv('all.csv')