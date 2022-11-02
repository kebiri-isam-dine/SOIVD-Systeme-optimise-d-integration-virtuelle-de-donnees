from contextlib import closing
from urllib.request import urlopen
import json
import dateutil.parser

WEATHER = {
	0: "Soleil",
	1: "Peu nuageux",
	2: "Ciel voilé",
	3: "Nuageux",
	4: "Très nuageux",
	5: "Couvert",
	6: "Brouillard",
	7: "Brouillard givrant",
	10: "Pluie faible",
	11: "Pluie modérée",
	12: "Pluie forte",
	13: "Pluie faible verglaçante",
	14: "Pluie modérée verglaçante",
	15: "Pluie forte verglaçante",
	16: "Bruine",
	20: "Neige faible",
	21: "Neige modérée",
	22: "Neige forte",
	30: "Pluie et neige mêlées faibles",
	31: "Pluie et neige mêlées modérées",
	32: "Pluie et neige mêlées fortes",
	40: "Averses de pluie locales et faibles",
	41: "Averses de pluie locales",
	42: "Averses locales et fortes",
	43: "Averses de pluie faibles",
	44: "Averses de pluie",
	45: "Averses de pluie fortes",
	46: "Averses de pluie faibles et fréquentes",
	47: "Averses de pluie fréquentes",
	48: "Averses de pluie fortes et fréquentes",
	60: "Averses de neige localisées et faibles",
	61: "Averses de neige localisées",
	62: "Averses de neige localisées et fortes",
	63: "Averses de neige faibles",
	64: "Averses de neige",
	65: "Averses de neige fortes",
	66: "Averses de neige faibles et fréquentes",
	67: "Averses de neige fréquentes",
	68: "Averses de neige fortes et fréquentes",
	70: "Averses de pluie et neige mêlées localisées et faibles",
	71: "Averses de pluie et neige mêlées localisées",
	72: "Averses de pluie et neige mêlées localisées et fortes",
	73: "Averses de pluie et neige mêlées faibles",
	74: "Averses de pluie et neige mêlées",
	75: "Averses de pluie et neige mêlées fortes",
	76: "Averses de pluie et neige mêlées faibles et nombreuses",
	77: "Averses de pluie et neige mêlées fréquentes",
	78: "Averses de pluie et neige mêlées fortes et fréquentes",
	100: "Orages faibles et locaux",
	101: "Orages locaux",
	102: "Orages fort et locaux",
	103: "Orages faibles",
	104: "Orages",
	105: "Orages forts",
	106: "Orages faibles et fréquents",
	107: "Orages fréquents",
	108: "Orages forts et fréquents",
	120: "Orages faibles et locaux de neige ou grésil",
	121: "Orages locaux de neige ou grésil",
	122: "Orages locaux de neige ou grésil",
	123: "Orages faibles de neige ou grésil",
	124: "Orages de neige ou grésil",
	125: "Orages de neige ou grésil",
	126: "Orages faibles et fréquents de neige ou grésil",
	127: "Orages fréquents de neige ou grésil",
	128: "Orages fréquents de neige ou grésil",
	130: "Orages faibles et locaux de pluie et neige mêlées ou grésil",
	131: "Orages locaux de pluie et neige mêlées ou grésil",
	132: "Orages fort et locaux de pluie et neige mêlées ou grésil",
	133: "Orages faibles de pluie et neige mêlées ou grésil",
	134: "Orages de pluie et neige mêlées ou grésil",
	135: "Orages forts de pluie et neige mêlées ou grésil",
	136: "Orages faibles et fréquents de pluie et neige mêlées ou grésil",
	137: "Orages fréquents de pluie et neige mêlées ou grésil",
	138: "Orages forts et fréquents de pluie et neige mêlées ou grésil",
	140: "Pluies orageuses",
	141: "Pluie et neige mêlées à caractère orageux",
	142: "Neige à caractère orageux",
	210: "Pluie faible intermittente",
	211: "Pluie modérée intermittente",
	212: "Pluie forte intermittente",
	220: "Neige faible intermittente",
	221: "Neige modérée intermittente",
	222: "Neige forte intermittente",
	230: "Pluie et neige mêlées",
	231: "Pluie et neige mêlées",
	232: "Pluie et neige mêlées",
	235: "Averses de grêle",
}


url1 = 'https://api.meteo-concept.com/api/forecast/daily?token=756f550d7a0f31da58721d31e518f252068b8c1e9a17c1d366d1e8e8edc405b2&insee=35238'
url2 = 'https://api.meteo-concept.com/api/forecast/daily/3/period/2?token=756f550d7a0f31da58721d31e518f252068b8c1e9a17c1d366d1e8e8edc405b2&amp;insee=31555'
url3 = 'https://api.meteo-concept.com/api/forecast/datetime?token=MON_TOKEN&insee=2019-01-01T19:00:00+0100'

print("\n ---------------------------------- \n")

# Localisation des villes 

with closing(urlopen('https://api.meteo-concept.com/api/location/city?token=756f550d7a0f31da58721d31e518f252068b8c1e9a17c1d366d1e8e8edc405b2&insee=31555')) as f:
	city = json.loads(f.read())['city']
	print(u'La ville de {} ({}) a pour coordonnées {},{}.'.format(city['name'], city['cp'], city['latitude'], city['longitude']))

print("\n ---------------------------------- \n")

# prévision météo à un endroit grâce au code insee
with closing(urlopen(url1)) as f:
	forecast = json.loads(f.read())['forecast']
	print(len(forecast))
	c = 0
	for x in forecast:
		if c != x['insee']:
			print("Le temps  à " , x['insee'], " est :", WEATHER[x['weather']])
		c = x['insee']

print("\n ---------------------------------- \n")

# prévision météo dans qlq jours 
with closing(urlopen(url2)) as f:
    forecast = json.loads(f.read())['forecast']
    print(u"Le temps prévu pour l'après-midi dans trois jours est : \"{}\"".format(WEATHER[forecast['weather']]))

print("\n ---------------------------------- \n")

# infos sur éphéméride
with closing(urlopen('https://api.meteo-concept.com/api/ephemeride/1?token=756f550d7a0f31da58721d31e518f252068b8c1e9a17c1d366d1e8e8edc405b2&insee=35238')) as f:
    cityEph = json.loads(f.read())
    print(u'Demain, à {}, le soleil se lèvera à {} et se couchera à {}.'.format(cityEph['city']['name'], cityEph['ephemeride']['sunrise'], cityEph['ephemeride']['sunset']))
    print(u'On comptera {} minutes de soleil de {} qu\'aujourd\'hui.'.format(abs(cityEph['ephemeride']['diff_duration_day']), 'moins' if cityEph['ephemeride']['diff_duration_day'] <= 0 else 'plus'))

print("\n ---------------------------------- \n")

# Prévisions météo par jour 
with closing(urlopen('https://api.meteo-concept.com/api/forecast/daily?token=756f550d7a0f31da58721d31e518f252068b8c1e9a17c1d366d1e8e8edc405b2&insee&insee=31555')) as f:
    decoded = json.loads(f.read())
    (city,forecast) = (decoded[k] for k in ('city','forecast'))

    saturday = None
    for i,f in enumerate(forecast):
        day = dateutil.parser.parse(f['datetime']).weekday() # Lundi : 0, Mardi : 1, etc.
        if day == 5:
            saturday = i
            break

    print(u"Le week-end prochain est dans {} jours ! Les températures mini/maxi à {} seront :".format(saturday, city['name']))
    print(u"\tSamedi   : {}°C/{}°C".format(forecast[saturday]['tmin'],forecast[saturday]['tmax']))
    print(u"\tDimanche : {}°C/{}°C".format(forecast[saturday+1]['tmin'],forecast[saturday+1]['tmax']))

print("\n ---------------------------------- \n")

#Prévisions météo par ville et  par heure 

with closing(urlopen('https://api.meteo-concept.com/api/forecast/nextHours?token=756f550d7a0f31da58721d31e518f252068b8c1e9a17c1d366d1e8e8edc405b2&insee=35238')) as f:
    forecast = json.loads(f.read())['forecast']
    print(u"Humidité relative de l'air (%)\n   ∧")
    for i in range(100, 0, -10):
        print(u"{: >3}│ ".format(i), end='')
        for f in forecast:
            if f['rh2m'] >= i:
                print(u"  █    ", end='')
            else:
                print(u"       ", end='')
        print("")
    print("   └─", end='')
    for f in forecast:
        print("───────", end='')
    print(">\n     ", end='')
    for f in forecast:
        print(dateutil.parser.parse(f['datetime']).strftime('%H:%M  '), end='')
    print("")



