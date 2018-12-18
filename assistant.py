import speech_recognition as sr
import os
import re
import webbrowser
import smtplib
import requests
from weather import Weather, Unit
import win32com.client as wincl
import pyttsx3
from urllib.request import urlopen
from bs4 import BeautifulSoup
import speedtest

def talkToMe(audio):

    print(audio)
    for line in audio.splitlines():
        engine = pyttsx3.init()
        engine.say(audio)
        engine.runAndWait()


def myCommand():
    "listens for commands"

    r = sr.Recognizer()

    with sr.Microphone() as source:
        print('Ready...')
        r.pause_threshold = 1
        r.adjust_for_ambient_noise(source, duration=1)
        audio = r.listen(source)

    try:
        command = r.recognize_google(audio).lower()
        print('You said: ' + command + '\n')

    #loop back to continue to listen for commands if unrecognizable speech is received
    except sr.UnknownValueError:
        print('I didnt hear that')
        command = myCommand();

    return command


def assistant(command):
    "if statements for executing commands"
    
    if 'open website' in command:
        reg_ex = re.search('open website (.+)', command)
        if reg_ex:
            domain = reg_ex.group(1)
            url = 'https://www.' + domain
            webbrowser.open(url)
            print('Done!')
        else:
            pass

    elif 'what\'s up' in command:
        talkToMe('Im good')
        
    elif 'joke' in command:
        res = requests.get(
                'https://icanhazdadjoke.com/',
                headers={"Accept":"application/json"}
                )
        if res.status_code == requests.codes.ok:
            talkToMe(str(res.json()['joke']))
        else:
            talkToMe('oops!I ran out of jokes')

    elif 'weather in' in command:
        reg_ex = re.search('current weather in (.*)', command)
        if reg_ex:
            city = reg_ex.group(1)
            weather = Weather(unit=Unit.CELSIUS)
            location = weather.lookup_by_location(city)
            condition = location.condition
            print(condition.text)
            print(condition.temp)
            talkToMe('The Current weather in %s is %s, The temprature is %s degrees celcious' % (city, condition.text, condition.temp))

    elif 'weather forecast in' in command:
        reg_ex = re.search('weather forecast in (.*)', command)
        if reg_ex:
            city = reg_ex.group(1)
            weather = Weather(unit=Unit.CELSIUS)
            location = weather.lookup_by_location(city)
            forecasts = location.forecast
            for forecast in forecasts:
             talkToMe('On %s it will be %s, The maximum temperture will be %s degrees, The lowest temperature will be %s degrees.' % (forecast.date , forecast.text , forecast.high , forecast.low))
             
    elif 'the time' in command:
        data = urlopen("https://api.thingspeak.com/apps/thinghttp/send_request?api_key=JKKQYRWRIC63DNLG")
        data = data.read()
        data = data.decode("utf-8")
        data = data.replace("b'", "")
        data = data.replace("'", "")
        talkToMe('the time is %s' % data)
        
    elif 'internet speed test' in command:
        talkToMe('testing... , this may take some time')
        speedtester = speedtest.Speedtest()
        speedtester.get_best_server()

        speed=speedtester.download()
        speed=speed/1000000
        speed=round(speed,2)
        talkToMe('your download speed is %s mega bits per second' % speed)
        
    elif 'fortnite wins' in command:
        wins = urlopen("https://api.thingspeak.com/apps/thinghttp/send_request?api_key=8QD0HJ1RDQT6KOMM")
        wins = wins.read()
        wins = wins.decode("utf-8")
        wins = wins.replace("<h3>", "")
        wins = wins.replace("</h3>", "")
        talkToMe('You have %s wins in total' % wins)
        
    else:
        talkToMe('I cant do that')
        print("I cant do that")

talkToMe('I am ready for your command')

#loop to continue executing multiple commands
while True:
    assistant(myCommand())
