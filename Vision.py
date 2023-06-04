import openai
import sys
import uuid
import win32gui
import datetime
import os
import time
import cv2
import pyautogui
import pyttsx3
import wikipedia
import webbrowser
import subprocess
import pywhatkit as kit
import speech_recognition as sr
import smtplib
from requests import get


engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice',voices[2].id)
engine.setProperty('rate',160)

def generate_response(prompt):
    openai.api_key ="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"
    response=openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=1000,
        n=1,
        stop=None,
        temperature=0.5,
    )
    return response['choices'][0]["text"] # type: ignore
    
def speak(audio):
    engine.say(audio)
    print(audio)
    engine.runAndWait()

def wish():
    hour = int(datetime.datetime.now().hour)
    if hour>=6 and hour<=12:
        speak("Good Morning")
    elif hour>12 and hour<16:
        speak("Good Afternoon")
    else:
        speak("Good Evening")
    speak("How May I Assist you ?" )



def takecommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.energy_threshold = 300 # adjust for ambient noise
        r.pause_threshold = 0.8 # reduce pause threshold
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source)
    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language='en-in')
        query = query.lower() # type: ignore
        print(f"User Said: {query}\n")
        
    except Exception as e:
        print('Say that again please...')
        return "none"
    
    return query



def Microsoft():
    app_commands = {
        'excel': 'Excel',
        'powerpoint': 'PowerPoint',
        'edge': 'Edge',
        'word': 'Word',
        'outlook': 'Outlook',
        'onenote': 'OneNote',
        'access': 'Access',
        'publisher': 'Publisher',
        'access': 'Access',
        'visio': 'Visio'
    }
    
    app = query.replace('open', '').replace('microsoft', '').strip() # type: ignore
    app_command = app_commands.get(app, None)
    
    if app_command is not None:
        app_path = fr"C:\ProgramData\Microsoft\Windows\Start Menu\Programs\{app_command}"
        os.startfile(app_path)
    else:
        print(f"Could not find application: {app}")
    time.sleep(3)

def write_information():
    if 'notepad' in query: # type: ignore
        subprocess.Popen('C:\\Windows\\Notepad.exe')
        response = generate_response(query)# type: ignore
        pyautogui.typewrite(response)
        speak(response)
        time.sleep(5)
    elif 'word' in query:# type: ignore
        app_path = fr"C:\ProgramData\Microsoft\Windows\Start Menu\Programs\Word"
        os.startfile(app_path)
        time.sleep(5)
        new_page()
        response = generate_response(query)# type: ignore
        pyautogui.typewrite(response)
        speak(response)
        time.sleep(5)
    else:
        subprocess.Popen('C:\\Windows\\Notepad.exe')
        response = generate_response(query) # type: ignore
        pyautogui.typewrite(response)
        speak(response)
        time.sleep(5)    


def ai():
    response = generate_response(query) 
    print(f"Vision Says: {response}")
    speak(response)

def text():
    text = query.replace('type', '') # type: ignore
    pyautogui.write(text,0.1)

def new_page():
    pyautogui.keyDown("ctrl")
    pyautogui.press("N")
    pyautogui.keyUp("ctrl")


def TaskExecution():
            
    wish()
    while 1:
        query=takecommand()
        if "open notepad" in query:
            subprocess.Popen('C:\\Windows\\Notepad.exe')
            time.sleep(3)

        elif "close notepad" in query:
            os.system("taskkill /f /im notepad.exe")

        elif "this PC" in query:
            npath = "C:\\Windows\\system32\\filemanager.exe"
            os.startfile(npath)
            time.sleep(3)

        

        elif 'open new page' in query:
            new_page()
            time.sleep(3)
            speak('Any thing else I can help you with')
            takecommand()
            if 'no' in query:
                speak('Okay')
                sys.exit(0)
            else:
                break

        elif 'message on whatsapp' in query:
            os.startfile("whatsapp://")
            speak('To whom should I send the message?')
            person = takecommand()
            pyautogui.typewrite(person, 0.1)
            pyautogui.press('down')
            pyautogui.press('enter')
            speak('What do you want to say?')
            while True:
                message = takecommand()
                if len(message)>1:
                    pyautogui.typewrite(message, 0.1)
                        #
                    speak('Anything else you want to type?')
                else:
                    speak('I did not understand. Please try again.')
                keepgoing = takecommand()
                if 'no' in keepgoing:
                    break
                elif 'delete' in keepgoing:
                    pyautogui.hotkey('ctrl', 'a')
                    pyautogui.press('backspace')
                    break
                else:
                    pyautogui.typewrite(keepgoing, 0.1)
                    break
            pyautogui.press('enter')
            speak('Message sent. Anything else I can help you with?')

        elif "email" in query:
            speak("Who is the recipient? ")
            recipient = takecommand()
            if "me" in recipient:
                try:
                    speak("What should I say? ")
                    content = takecommand()
                    server = smtplib.SMTP("smtp.gmail.com", 587)
                    server.ehlo()
                    server.starttls()
                    server.login("Your_Username", "Your_Password")
                    server.sendmail("Your_Username", "Recipient_Username", content)
                    server.close()
                    speak("Email sent!")
                except Exception:
                    speak("Sorry Sir! I am unable to send your message at this moment!")

        elif 'open whatsapp' in query:
            os.startfile("whatsapp://")

        elif 'new file' in query:
            pyautogui.hotkey('ctrl', 'n')
            pyautogui.press('enter')
            
        elif "open excel" in query:
            app_path = fr"C:\ProgramData\Microsoft\Windows\Start Menu\Programs\Excel"
            os.startfile(app_path)
            if "new" in query:
                new_page()

        elif "open word" in query:
            app_path = fr"C:\ProgramData\Microsoft\Windows\Start Menu\Programs\Word"
            os.startfile(app_path)
            if "new" in query:
                new_page()
            time.sleep(2)

        elif "open powerPoint" in query:
            app_path = fr"C:\ProgramData\Microsoft\Windows\Start Menu\Programs\PowerPoint"
            os.startfile(app_path)
            if "new" in query:
                new_page()
            time.sleep(2)
            

        elif "open microsoft edge" in query:
            app_path = fr"C:\ProgramData\Microsoft\Windows\Start Menu\Programs\Edge"
            os.startfile(app_path)
            time.sleep(1)
            if "new" in query:
                new_page()
                time.sleep(2)
    
        elif "open firefox" in query:
            npath = r"C:\Program Files\Mozilla Firefox\firefox.exe"
            os.startfile(npath)
            time.sleep(5)
            if "new" in query:
                new_page()
                time.sleep(2)

        elif 'history' in query:
            pyautogui.hotkey('ctrl', 'h')

        elif 'downloads' in query:
            pyautogui.hotkey('ctrl', 'j')
        
        elif "open turbo C" in query:
            npath = r"C:\Program Files (x86)\Dev-Cpp\devcpp.exe"
            os.startfile(npath)

        elif "open VLC" in query:
            npath = r"C:\Program Files\VideoLAN\VLC\vlc"
            os.startfile(npath)

        elif 'press' in query:
              # Remove the word "press" from the query to get the key to be pressed
            key = query.replace('press', '').strip()

            # Simulate the key press using PyAutoGUI
            if 'enter' in key:
                pyautogui.press('enter')
            elif 'tab' in key:
                pyautogui.press('tab')
            elif 'backspace' in key:
                pyautogui.press('backspace')
            elif 'space' in key:
                pyautogui.press('space')
            elif 'up' in key:
                pyautogui.press('up')
            elif 'down' in key:
                pyautogui.press('down')
            elif 'left' in key:
                pyautogui.press('left')
            elif 'right' in key:
                pyautogui.press('right')
            else:
                print("Unknown key")

            # Print a message to indicate the key press was successful
            print(f"{key.capitalize()} key pressed successfully!")

        elif 'scroll up' in query:
            # Simulate a scroll up
            pyautogui.scroll(-1000)

        elif "chrome" in query:
            url = 'https://www.google.com'

            # Specify the path to the Chrome executable on your system
            chrome_path = '/Applications/Google Chrome.app %s' # Update this with the path to your Chrome executable

            # Open the URL in a new Chrome window
            webbrowser.get(chrome_path).open_new(url)
        
        elif "command prompt" in query:
            os.system("start cmd.exe")
            
        elif "close command prompt" in query:
            os.system("taskkill /f /im cmd.exe")

        elif "camera" in query:
            cap = cv2.VideoCapture(0)
            while True:
                ret, im =cap.read()
                cv2.imshow('webcam',im)
                k = cv2.waitKey(10)
                if k==3:
                    break
            cap.release()
            cv2.destroyAllWindows()
            
        elif 'ip address' in query:
            ip = get("https://api64.ipify.org").text  
            speak(f"Your IP Adress is "+ip)
        
        
        elif "wikipedia" in query:
            speak('Searching wikipedia...')
            query = query.replace("wikipedia" , '')
            result = wikipedia.summary(query, sentences=2)
            speak("Accorging to wikidepia")
            speak(result)
            time.sleep(2)

        elif "open" in query:
            if "code" in query:
                os.startfile("C:\\Users\\USER\\AppData\\Local\\Programs\\Microsoft VS Code\\Code.exe")
            elif "github" in query:
                webbrowser.open("https://www.github.com")
            elif "facebook" in query:
                webbrowser.open("https://www.facebook.com")
            elif "instagram" in query:
                webbrowser.open("https://www.instagram.com")
            
            elif "youtube" in query:
                webbrowser.open("https://www.youtube.com")
            elif "google" in query:
                webbrowser.open("https://www.google.com")
                speak("what should I search ?")
                item = takecommand().lower()
                webbrowser.open(f"{item}")
                results = wikipedia.summary(item, sentences=2)
                speak(results)

            elif "linkedin" in query:
                webbrowser.open("https://www.linkedin.com")
            elif "twitter" in query:
                webbrowser.open("https://www.twitter.com")
            elif "spotify" in query:
                os.system("spotify")
            time.sleep(3)
        
        elif 'close edge' in query:
            os.system("taskkill /f /im msedge.exe")
        elif 'close youtube' in query:
            os.system("taskkill /f /im msedge.exe")


        elif  'play' in query:
            query = query.replace('play online', '')
            kit.playonyt(query)   # type: ignore
        
        elif 'play songs' in query:
            song = query.replace('play', '')
            speak('playing ' + song)
            kit.playonyt(song)   # type: ignore

        elif "switch the window" in query:
            pyautogui.keyDown("alt")
            pyautogui.press("tab")
            time.sleep(1)
            pyautogui.keyUp("alt")

        elif 'minimise' in query:
            pyautogui.hotkey('alt', 'space')
            time.sleep(1)
            pyautogui.press('n')


        elif "today's date" in query:
            strDate = datetime.datetime.now().strftime("%d-%m-%Y")
            speak(f"Sir, today's date is {strDate}")

        elif "the time" in query:
            strTime = datetime.datetime.now().strftime("%H:%M:%S")
            speak(f"Sir, the time is {strTime}")
        
        elif "take a screenshot" in query:
            time.sleep(3)
            img = pyautogui.screenshot()
            filename = f"{uuid.uuid4()}.png"
            img.save(filename)
            speak(f"The screenshot is saved as {filename} in the main folder.")

        elif 'write' in query:
            if 'notepad' in query:
                subprocess.Popen('C:\\Windows\\Notepad.exe')
                response = generate_response(query)
                pyautogui.write(response,0.1)
            elif 'word' in query:
                app_path = fr"C:\ProgramData\Microsoft\Windows\Start Menu\Programs\Word"
                os.startfile(app_path)
                time.sleep(5)
                new_page()
                response = generate_response(query)
                pyautogui.write(response,0.1)
            else:
                subprocess.Popen('C:\\Windows\\Notepad.exe')
                response = generate_response(query)
                pyautogui.write(response,0.1)

        elif "volume up" in query:
            pyautogui.press("volumeup")
            pyautogui.press("volumeup")
            pyautogui.press("volumeup")
            pyautogui.press("volumeup")
            pyautogui.press("volumeup")
            pyautogui.press("volumeup")
            pyautogui.press("volumeup")
            pyautogui.press("volumeup")
            pyautogui.press("volumeup")
            pyautogui.press("volumeup")
            pyautogui.press("volumeup")
            pyautogui.press("volumeup")
            pyautogui.press("volumeup")
            pyautogui.press("volumeup")
            pyautogui.press("volumeup")

        elif "volume down" in query:
            pyautogui.press("volumedown")
            pyautogui.press("volumedown")
            pyautogui.press("volumedown")
            pyautogui.press("volumedown")
            pyautogui.press("volumedown")
            pyautogui.press("volumedown")
            pyautogui.press("volumedown")
            pyautogui.press("volumedown")
            pyautogui.press("volumedown")
            pyautogui.press("volumedown")
            pyautogui.press("volumedown")
            pyautogui.press("volumedown")
            pyautogui.press("volumedown")
            pyautogui.press("volumedown")
            pyautogui.press("volumedown")

        elif "mute" in query:
            pyautogui.press("volumemute")

        elif'close tab' in query:
            pyautogui.hotkey('ctrl')
            time.sleep(1)
            pyautogui.press('w')

        elif 'browsing history' in query:
            pyautogui.hotkey('ctrl')
            time.sleep(1)
            pyautogui.press('h')
        
        elif'browser downloads' in query:
            pyautogui.hotkey('ctrl')
            time.sleep(1)
            pyautogui.press('j')
        
        elif "scroll down" in query:
            pyautogui.scroll(1000)

        elif "who are you" in query:
            speak('My Name Is Vision')
            speak('I can Do Everything that my creator programmed me to do')


        elif 'type' in query:
            while True:
                speak('What do you want to type ?')
                query = takecommand()
                if len(query)>1:
                    pyautogui.typewrite(query, 0.1)
                    speak('Anything else you want to type?')
                    query = takecommand()
                    if 'no' in query:
                        break
                    elif 'yes' in query:
                        speak('Please Continue ')
                        query = takecommand()
                        pyautogui.typewrite(query, 0.1)
                        break
                    else:
                        pyautogui.typewrite(query, 0.1)
                        break
                else:
                    speak('I did not understand. Please try again.')
                            
        elif "thank you" in query:
            speak("You're welcome!")

        elif "shutdown the system" in query:
            os.system("shutdown /s /t 1")
        
        elif "restart the system" in query:
            os.system("shutdown /r /t 1")

        elif "lock the system" in query:
            os.system("rund1l32.exe powrprof.dil,SetSusoendState 0,1,0")

        elif "exit" in query:
            speak("Goodbye!")
            sys.exit(0)

        elif len(query)>5:
            response = generate_response(query) 
            print(f"Vision Says: {response}")
            speak(response)


if __name__ == '__main__':
    TaskExecution()



