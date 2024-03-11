'''
Dependencias:
- pyttsx3
- SpeechRecognition
- PyAudio
- pywhatkit
- subprocess
- psutil
- pickle
'''

''' Crear el ejecutable con el siguiente comando: pyinstaler --windowed --onefile --icon:ruta/del/icono '''


import pyttsx3
import speech_recognition as sr
import datetime
import pywhatkit
import subprocess
import json
import os
import datetime


listener = sr.Recognizer()
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)
engine.setProperty('rate', 140)

# Función para hablar
def talk(text):
    engine.say(text)
    engine.runAndWait()

# Función para "escuchar"
def take_command():
    try:
        with sr.Microphone() as source:
            print("Escuchando...")
            voice = listener.listen(source)
            command = listener.recognize_google(voice, language = 'ES')
            command = command.lower()
            print(command)
            return command
    except Exception as e:
        print(e)
        return ""
# Saludo
def greeting():
    current_time = datetime.datetime.now()
    hour = current_time.hour
    if 4 <= hour <= 15:
        talk("Buenos días usuario") 
    elif 15 <= hour <= 20 :
        talk("Buenas tardes usuario")
    else:
        talk("Buenas noches usuario")  

# Función de anotación
def notas():
    try:
        now = datetime.datetime.now()
        nombre_nota = f"nota_{now.strftime('%Y%m%d_%H%M%S')}.txt"

        with open(nombre_nota, "a") as file:
            while True:
                talk("Dicta lo que quieras agregar a la nota. Di 'terminar nota' para finalizar.")
                command = take_command()
                if "terminar nota" in command:
                    talk("Nota finalizada.")
                    break
                else:
                    file.write(command + "\n")
                    talk("Nota actualizada.")

        talk("Se ha guardado la nota correctamente.")

    except Exception as e:
        print("Error:", e)
        talk("Ocurrió un error al tomar notas. Por favor, inténtalo de nuevo más tarde.")
# Función que comprueba lo que se va diciendo
def run_assistant():
    command = take_command()
    # Saludo
    if "hola" in command:
        talk("hola, usuario")
        # Poner música
    elif "pon" in command:
        cancion = command.replace("pon", "")
        talk(f"poniendo {command}")
        pywhatkit.playonyt(cancion)
        # Escribir notas de voz
    elif "escribe" in command:
        talk(f"Te escucho.")
        notas()

   # Abrir aplicación
    elif command.lower().startswith("abre"):
        app_commands = {
            "google":f"{os.path.join(os.environ.get('LOCALAPPDATA'), 'Vivaldi', 'Application', 'vivaldi.exe')}",
            "discord":f"{os.environ.get('LOCALAPPDATA')}\Discord\app-1.0.9030\Discord.exe"
        }
        app_name = command.split(" ",1)[-1].lower() #IMPORTANTE

        if app_name in app_commands:
            talk(f"abriendo {app_name}")
            subprocess.Popen(app_commands[app_name])
        else:
            talk(f"No se encontró la aplicación: {app_name}")
    # Salir del programa
    elif "adiós" in command:
        talk("Adiós, usuario")
        exit()

        
greeting()
print(datetime.datetime.now().hour)

while True:
    run_assistant()
