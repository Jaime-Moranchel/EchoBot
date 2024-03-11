# EchoBot

El siguiente código es un programa asistente que utiliza el reconocimiento de voz y la conversión de texto a voz para interactuar con el usuario. Realiza varias tareas basándose en las órdenes del usuario.

## Dependencias
El código requiere la instalación de las siguientes dependencias:
- pyttsx3
- SpeechRecognition
- PyAudio
- pywhatkit
- subprocess
- psutil
- pickle

## INSTRUCCIONES DE IMPORTACIÓN

~~~~
import pyttsx3
import speech_recognition as sr
import datetime
import pywhatkit
import subprocess
import json
import os
~~~~
- `pyttsx3`: Necesario para la conversión de texto a voz.
- `speech_recognition`: Necesario para la función de reconocimiento de voz.
- `datetime`: Necesario para acceder a la fecha y hora actuales.
- `pywhatkit`: Necesario para reproducir vídeos de YouTube.
- `subprocess`: Necesario para ejecutar comandos y programas externos.
- `json`: Necesario para leer y escribir archivos JSON.
- `os`: Necesario para acceder a las funciones relacionadas con el sistema.
  
## VARIABLES

~~~~
listener = sr.Recognizer()
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)
engine.setProperty('rate', 140)
~~~~
- `listener`: Una instancia de la clase Recognizer del módulo speech_recognition. Se utiliza para capturar la entrada de audio.
- `engine`: Una instancia de la clase Engine del módulo pyttsx3. Se utiliza para la conversión de texto a voz.
- `voices`: Lista de voces disponibles para la conversión de texto a voz.
- `voice`: Establece la voz del asistente en la primera voz de la lista de voces.
- `rate`: Ajusta la velocidad del habla del asistente.

## FUNCIONES AUXILIARES

### `talk(text)`

~~~~
def talk(text):
    engine.say(text)
    engine.runAndWait()
~~~~
- `text` (str): El texto que pronunciará el asistente.
Esta función utiliza la instancia `engine` para convertir el texto dado en voz y ejecutarlo.

### `take_command()`

~~~~
def take_command():
    try:
        with sr.Microphone() as source:
            print("Escuchando...")
            voice = listener.listen(source)
            command = listener.recognize_google(voice, language='ES')
            command = command.lower()
            print(command)
            return command
    except Exception as e:
        print(e)
        return ""
~~~~
Esta función utiliza la instancia `listener` para escuchar la entrada de voz del micrófono. A continuación, utiliza el método `recognize_google()` de la instancia de `listener` para convertir la entrada de voz en texto. El texto reconocido se devuelve como comando.

### `greeting()`

~~~~
def greeting():
    current_time = datetime.datetime.now()
    hour = current_time.hour
    if 4 <= hour <= 15:
        talk("Buenos días usuario") 
    elif 15 <= hour <= 20 :
        talk("Buenas tardes usuario")
    else:
        talk("Buenas noches usuario")
~~~~
Esta función saluda al usuario basándose en la hora actual. La función obtiene la hora actual usando el método `datetime.datetime.now()` y luego comprueba el valor de la hora para determinar el saludo apropiado.

### `notas()`

~~~~
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
~~~~
Esta función permite al usuario tomar notas. Crea un nuevo archivo de notas con un nombre que incluye la fecha y hora actuales. La función escucha continuamente las entradas del usuario y las escribe en el fichero de notas. El usuario puede terminar el proceso de toma de notas diciendo "terminar nota". El fichero de notas se guarda en el directorio actual.

### `run_assistant()`

~~~~
def run_assistant():
    command = take_command()
    if "hola" in command:
        talk("hola, usuario")
    elif "pon" in command:
        cancion = command.replace("pon", "")
        talk(f"poniendo {command}")
        pywhatkit.playonyt(cancion)
    elif "escribe" in command:
        talk(f"Te escucho.")
    elif "discos" in command:
        subprocess.run(['powershell.exe', '-File', '.\utilidades\disk_info\disk_info.ps1'])
        subprocess.run(['notepad.exe', '.\drives.json'])
    elif command.lower().startswith("abre"):
        app_commands = {
            "google":f"{os.path.join(os.environ.get('LOCALAPPDATA'), 'Vivaldi', 'Application', 'vivaldi.exe')}",
            "discord":f"{os.path.join(os.environ.get('LOCALAPPDATA'),'Discord', 'app-1.0.9035', 'Discord.exe')}"
        }
        app_name = command.split(" ",1)[-1].lower() #IMPORTANT

        if app_name in app_commands:
            talk(f"abriendo {app_name}")
            subprocess.Popen(app_commands[app_name])
        else:
            talk(f"No se encontró la aplicación: {app_name}")

    elif "adiós" in command:
        talk("Adiós, usuario")
        exit()
~~~~
Esta función es la función principal que ejecuta todas las tareas basadas en los comandos del usuario. Toma el comando del usuario usando la función `take_command()` y luego realiza varias acciones basadas en el comando.
- Si el comando es "hola", el asistente saluda al usuario con "hola, usuario".
- Si el comando empieza por "pon", el asistente extrae el nombre de la canción del comando y reproduce la canción en YouTube mediante la función `pywhatkit.playonyt()`.
- Si la orden es "escribe", el asistente reconoce la orden del usuario y vuelca todo lo que diga el usuario a un archivo mediante la función `notas()`.
- Si el comando es "discos", el asistente ejecuta un script de PowerShell `disk_info.ps1` para obtener información de disco y guarda el resultado en un archivo `drives.json`. A continuación, abre el archivo `drives.json` con el Bloc de notas.
- Si el comando empieza por "abre", el asistente comprueba si el nombre de la aplicación después de "abre" existe en el diccionario `app_commands`. Si existe, el asistente abre la aplicación utilizando la función `subprocess.Popen()`. Si no existe, el asistente avisa al usuario.
- Si la orden es "adiós", el asistente dice "Adiós, usuario" y sale del programa.

## EJECUCIÓN PRINCIPAL

~~~~
greeting()
print(datetime.datetime.now().hour)

while True:
    run_assistant()
~~~~
La ejecución principal comienza con la función `greeting()` para saludar al usuario. Luego entra en un bucle infinito donde la función `run_assistant()` es llamada repetidamente para escuchar y ejecutar los comandos del usuario. El bucle se ejecuta hasta que el usuario dice "adiós".