from urllib.request import urlopen, Request
import time
import datetime
import urllib.parse
import ast
import re


def get_weather(place):
    place = place.lower()
    w = ''
    if 'overcast' in place:
        w = w + 'bedeckt'
    elif 'cloud' in place or 'cloudy' in place or 'clouds' in place:
        if 'scattered' in place or 'broken' in place or 'few' in place:
            w = w + 'teils wolkig'
        else:
            w = w + 'wolkig'
    elif 'drizzle' in place:
        w = w + 'leichten Nieselregen'
    elif 'clear' in place:
        w = w + 'klar'
    elif 'rain' in place or 'rainy' in place:
        if 'light' in place:
            w = w + 'leichten Regen'
        elif 'heavy' in place:
            w = w + 'starken Regen'
        else:
            w = w + 'regnerisch'
    elif 'mist' in place or 'misty' in place:
        w = w + 'neblig'
    elif 'haze' in place:
        w = w + 'leichten Dunst'
    elif 'hail' in place:
        w = w + 'Heil Hydra'
    elif 'smoke' in place:
        w = w + 'einen Waldbrand geben'
    elif 'storm' in place or 'stormy' in place:
        w = w + 'stürmisch'
    elif 'thunderstorm' in place:
        w = w + 'Gewitter'
    elif 'snow' in place or 'snowy' in place or 'snowfall' in place:
        if 'heavy' in place:
            w = w + 'starken Schneefall'
        elif 'light' in place:
            w = w + 'leichten Schneefall'
        else:
            w = w + 'Schneefall'
    else:
        w = w + place
    return w



def get_temperature(pl):
    t = pl - 272.15
    t = str(t)[:2]
    return t

def zeitabfrage(dic):
    now = datetime.datetime.now()
    time = dic.get('datetime')
    differenz = time - now
    if differenz.total_seconds() >= 40*10800:
        time = 'Ich kann leider nicht so weit in die Zukunft sehen.' #Möchtest du wissen, wie das Wetter in 5 Tagen wird?
    return time


def handle(text, core, skills):
    now = datetime.datetime.now()
    o = core.analysis['town']
    if o == None:
        core.say('Für welchen Ort möchtest du das Wetter erfahren?')
        antwort = core.listen()
        if antwort == 'TIMEOUT_OR_INVALID':
            core.say('Ich konnte den Ort leider nicht verstehen')
        else:
            antwort = antwort.lower()
            if len(antwort.split()) == 1:
                o = antwort
            elif 'hier' in antwort or 'zu hause' in antwort:
                o = core.local_storage['home_location'].lower()
            else:
                sonst = 'der dem den einer'
                satz = {}
                mind = 0
                falsches_in = 0
                i = str.split(antwort)
                ind = 1
                for w in i:
                    satz[ind] = w
                    ind += 1
                for iindex, word in satz.items():
                    if word in sonst:
                        mind = mind + iindex
                for iindex, word in satz.items():
                    if iindex == mind - 1:
                        falsches_in = falsches_in + iindex
                if falsches_in >= 1:
                    del satz[falsches_in]
                for iindex, word in satz.items(): #findet Wort 'in''s key
                    if word == 'in':
                        in_index = iindex
                        myind = in_index + 1
                        o = satz.get(myind)
                    elif word == 'für':
                        für_index = iindex
                        myind = für_index + 1
                        o = satz.get(myind)
    else:
        o = o
    ort = o.lower()
    web = 'http://api.openweathermap.org/data/2.5/forecast?q=' + urllib.parse.quote(ort) + '&appid=bd4d17c6eedcff6efc70b9cefda99082'
    request = Request(web)
    try:
        response = urlopen(request)
    except:
        core.say('Ich konnte das Wetter für den Ort {} leider nicht aufrufen.'.format(o))
        return
    html = response.read()
    html = str(html)
    ohneb = html[2:len(html)-1]
    wetterdictionary = ast.literal_eval(ohneb)
    zeit = zeitabfrage(core.analysis) #dt_txt = zeit
    if zeit == 'Ich kann leider nicht so weit in die Zukunft sehen.': #Möchtest du wissen, wie das Wetter in 5 Tagen wird muss ich noch rauslassen, weil ich nicht weiÃŸ, wie ich dann mit der Antwort umgehen muss
        core.say(zeit)
        '''antwort = core.listen()
        antwort = antwort.lower()
        if 'ja' in antwort:'''

    else:
        weatherdescription = ''
        liste_der_wetterbeschreibungen = wetterdictionary.get('list')
        minimum = 0
        maximum = 0
        for item in liste_der_wetterbeschreibungen:
            genannte_zeit = zeitabfrage(core.analysis)
            zeit_im_api = item.get("dt_txt") + '0000'
            zeit_im_api = datetime.datetime.strptime(zeit_im_api, "%Y-%m-%d %H:%M:%f")
            differenz = zeit_im_api - genannte_zeit
            if differenz.total_seconds() <= 10800 and differenz.total_seconds() >= 0:
                temperaturzeile = item.get("main")
                temp_min = temperaturzeile.get("temp_min")
                temp_max = temperaturzeile.get("temp_max")
                minimum = get_temperature(int(temp_min)) #
                if minimum[1] == '.':
                    minimum = minimum[0]
                maximum = get_temperature(int(temp_max)) #
                if maximum[1] == '.':
                    maximum = maximum[0]
                wetterzeile = item.get("weather")
                wetterdictionary = wetterzeile[0]
                beschreibung = wetterdictionary.get("description")
                weatherdescription = get_weather(beschreibung)
                break
        minimum = str(minimum)
        maximum = str(maximum)
        if weatherdescription == 'bedeckt' or weatherdescription == 'teils wolkig' or weatherdescription == 'wolkig' or weatherdescription == 'klar' or weatherdescription == 'regnerisch' or weatherdescription == 'neblig' or weatherdescription == 'einen Waldbrand geben' or weatherdescription == 'stürmisch':
            if minimum != maximum:
                wetter = 'In ' + ort + ' wird es ' + weatherdescription + ' bei ' + minimum + ' bis ' + maximum + ' Grad Celsius.'
            else:
                wetter = 'In ' + ort + ' wird es ' + weatherdescription + ' bei ' + minimum + ' Grad Celsius.'
        else:
            if minimum != maximum:
                wetter = 'In ' + ort + ' gibt es ' + weatherdescription + ' bei ' + minimum + ' bis ' + maximum + ' Grad Celsius.'
            else:
                wetter = 'In ' + ort + ' gibt es ' + weatherdescription + ' bei ' + minimum + ' Grad Celsius.'
        core.say(wetter)

    response.close()

def isValid(text):
    text = text.lower()
    if 'wird' in text:
        if 'wetter' in text or 'temperatur' in text or ' warm ' in text or ' kalt ' in text:
            return True

