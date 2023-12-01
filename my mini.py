import pyttsx3
import speech_recognition as sr 
import datetime
import wikipedia 
import webbrowser
import os
import smtplib
import requests
import pywhatkit
import pyjokes
import subprocess
import psutil
from pytube import YouTube
from requests import get
from urllib.parse import quote

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
# print(voices[1].id)
engine.setProperty('voice', voices[0].id)


def speak(audio):
    engine.say(audio)
    engine.runAndWait()


def wishMe():
    hour = int(datetime.datetime.now().hour)
    if hour>=0 and hour<12:
        speak("Good Morning Bhuvan, have a nice day!")

    elif hour>=12 and hour<18:
        speak("Good Afternoon Bhuvan, hope you had a good lunch!")   

    else:
        speak("Good Evening Bhuvan Sir!")  

    speak("I am Vivian. Please tell me how may I help you")       

def takeCommand():

    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source)

    try:
        print("Recognizing...")    
        query = r.recognize_google(audio, language='en-in')
        print(f"Bhuvan said: {query}\n")

    except Exception as e:
        # print(e)    
        print("Say that again please...")  
        return "None"
    return query

def sendEmail(to, content):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.login('bhuvan.dumpmail@gmail.com', 'Bhuvan@2001')
    server.sendmail('bhuvan.dumpmail@gmail.com', to, content)
    server.close()

if __name__ == "__main__":
    wishMe()
    while True:
        query = takeCommand().lower()

        if 'wikipedia' in query:
            speak('Searching Wikipedia...')
            query = query.replace("wikipedia", "")
            results = wikipedia.summary(query, sentences=2)
            speak("According to Wikipedia")
            print(results)
            speak(results)

        elif 'open youtube' in query:
            webbrowser.open("youtube.com")

        elif 'open google' in query:
            webbrowser.open("google.com")

        elif 'send a whatsapp message' in query:
            now = datetime.datetime.now()
            chour = now.strftime("%H")

            speak("Tell the Mobile No of Receiver")
            numbers = takeCommand()
            speak("Tell the Message you wanna send")
            message = takeCommand()
            #hours=int(input('Tell the hour as a number'))
            #minutes=int(input('Tell the hour as a number'))
            current_hour = int(now.strftime("%H"))
            current_minute = int(now.strftime("%M"))
            
            if numbers and message:
                pywhatkit.sendwhatmsg(numbers, message, current_hour, current_minute)

        elif 'open erp' in query:
            webbrowser.open("http://202.160.160.58:8080/lastudentportal/students/loginManager/youLogin.jsp")
            
        
    
        elif 'internet passwords' in query:
            try:
                data = (
                    subprocess.check_output(["netsh", "wlan", "show", "profiles"])
                    .decode("utf-8", errors="ignore")
                    .split("\n")
                )
                profiles = [i.split(":")[1][1:-1] for i in data if "All User Profile" in i]

                last_n_profiles = profiles[-10:]

                for profile in last_n_profiles:
                    results = (
                        subprocess
                        .check_output(["netsh", "wlan", "show", "profile", profile, "key=clear"])
                        .decode("utf-8", errors="ignore")
                        .split("\n")
                    )
                    passwords = [line.split(":")[1][1:-1] for line in results if "Key Content" in line]

                    try:
                        password_info = "{:<30}|  {:<}".format(profile, passwords[0])
                        print(password_info)
                        engine.say(password_info)
                        engine.runAndWait()
                    except IndexError:
                        password_info = "{:<30}|  {:<}".format(profile, "")
                        print(password_info)

            except subprocess.CalledProcessError as e:
                print(f"Error: {e}")


        elif 'local music' in query:
            music_dir = 'C:/Users/bhuva/OneDrive/Documents/bhu'
            songs = os.listdir(music_dir)
            print(songs)    
            os.startfile(os.path.join(music_dir, songs[0]))

        elif 'the time' in query:
            strTime = datetime.datetime.now().strftime("%H:%M:%S")    
            speak(f"Bhuvan, the time is {strTime}")

           
            
        elif 'who is your best friend' in query:
            speak("Bhuvan, my best friend is Siri. Besides Siri,I am friends with Alexa and Cortona. BUt Iam jealous of their capabilities and wish to become like them oneday")    

        elif 'email' in query:
            try:
                speak("What should I say?")
                content = takeCommand()
                to = "bhuvanchandramothe@gmail.com"    
                sendEmail(to, content)
                speak("Email has been sent!")
            except Exception as e:
                print(e)
                speak("Due to recent changes in Google's policy to prevent login with just username and password, I am unable to login and send the email")  
        
        elif 'play' in query:
            song = query.replace('play', '')
            speak('playing ' + song)
            pywhatkit.playonyt(song)

        elif 'time' in query:
            time = datetime.datetime.now().strftime('%I:%M %p')
            speak('Current time is ' + time)

        elif 'who is' in query:
            person = query.replace('who is', '')
            info = wikipedia.summary(person, 1)
            print(info)
            speak(info)

        elif 'location' in query:
            speak("Wait Bhuvan, let me check")
            try:
                IP_Address = get('https://api.ipify.org').text
                print(IP_Address)               
                sanitized_ip = quote(IP_Address, safe='')    # Remove special characters from IP_Address        
                url = f'https://get.geojs.io/v1/ip/geo/{sanitized_ip}.json'
                print(url)
                geo_request = get(url)
                geo_data = geo_request.json()                
                city = geo_data['city']
                state = geo_data['region']
                country = geo_data['country']
                tZ = geo_data['timezone']
                
                longitude = geo_data['longitude']
                latitude = geo_data['latitude']
                org = geo_data['organization_name']               
                print(city, state, country, tZ, longitude, latitude, org)               
                speak(f"Bhuvan, I am not sure, but I think we are in {city} city of {state} state of {country} country.")
                speak(f"And Bhuvan, we are in {tZ} timezone. The latitude of our location is {latitude}, and the longitude is {longitude}. We are using {org}'s network.")                
            except Exception as e:
                speak("Sorry Bhuvan, due to a network issue, I am not able to find where we are.")
                pass

        elif 'do my homework' in query:
            speak('sorry, I have a headache')

        elif 'how are you vivian' in query:
            speak("I am doing good by the grace of wifi gods, Hope you are doing good too.")

        elif 'how to get good package' in query:
            speak('poi chaduvuko first, tharvatha, anney ,avvey ,vasthay')

        elif 'What is your boyfriends name' in query:
            speak("I am feeling shy, but he is development stage.And we are going to marry after he passes testing")

        elif 'joke' in query:
            speak(pyjokes.get_joke())

        elif 'condition' in query:
            usage = str(psutil.cpu_percent())
            speak("CPU is at"+usage+" percentage")
            battery = psutil.sensors_battery()
            percentage = battery.percent
            speak(f"Bhuvan our system have {percentage} percentage Battery")
            if percentage >=75:
                speak(f"Bhuvan we could have enough charging to continue our work")
            elif percentage >=40 and percentage <=75:
                speak(f"Bhuvan we should connect out system to charging point to charge our battery")
            elif percentage >=15 and percentage <=30:
                speak(f"Bhuvan we don't have enough power to work, please connect to charging")
            else:
                speak(f"Bhuvan we have very low power, please connect to charging otherwise the system will shutdown very soon")

        # elif 'take rest' or 'sleep' in query:
        #     speak("Thanks for using me Bhuvan, have a good day")
        #     exit()
            
        elif 'exit' in query:
            break

        else:
            speak('Please say the command again.')