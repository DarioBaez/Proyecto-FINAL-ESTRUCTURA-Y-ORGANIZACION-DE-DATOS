import pyaudio
import os
import wave
import speech_recognition as RECo
from grafo import Grafo as gF
from grafo import Arista as aR
import sqlite3 as sQ
from gtts import gTTS

def Convertir_texto():
    # Configura las constantes
    FORMATO = pyaudio.paInt16
    CANALES = 1   #Se usa 1 para canal mono, 2 para canal stereo
    RATE = 44100   #Esta es la frecuencia de muestreo
    CHUNK = 1024   #Numero de cuadros de audio por buffer
    SEGUNDOS_GRABACION = 5  #El numero de segundos que durara la grabacion de voz
    NOMBRE_ARCHIVO_SALIDA = "grabacion.mp3" #EL nombre que se le dara a la grabacion para guardarlo, 

    # Inicia PyAudio
    audio = pyaudio.PyAudio()

    # Inicia la grabación
    flujo = audio.open(format=FORMATO, channels=CANALES, #crea un objeto llamado flujo que sonectara al microfono, con los parametros ya inicializados
                    rate=RATE, input=True,
                    frames_per_buffer=CHUNK)
    print("grabando voz...")
    cuadros = []

    for i in range(0, int(RATE / CHUNK * SEGUNDOS_GRABACION)):
        datos = flujo.read(CHUNK)
        cuadros.append(datos)          #ESta lista almacena por 5 segundos,varios cuadros de 1024 datos extraidos del microfono
    print("grabación de voz terminada")

    # Detiene la grabación
    flujo.stop_stream() #Detiene la grabacion
    flujo.close() #Cierra la grabacion
    audio.terminate() #Cierra la conexion al sistema de audio (mic y altavoces)

    #-------------------------------------------------------SE TRANSFORMA A WAV-----------------------------------------------
    # Guarda la grabación en un archivo WAV
    archivo_wave = wave.open(NOMBRE_ARCHIVO_SALIDA, 'wb') #Abre el archivo de tipo .wav en escritura binaria
    archivo_wave.setnchannels(CANALES)                    #Este metodo le pone los canales en los que va a trabajar el audio
    archivo_wave.setsampwidth(audio.get_sample_size(FORMATO))
    archivo_wave.setframerate(RATE)
    archivo_wave.writeframes(b''.join(cuadros))           #La grabacion relizada por el microfono y guardada en la lista cuadros, se guardara en un archivo de tipo .wav
    archivo_wave.close()                                #Se cierra el archivo ya modificado


    #-------------------------------------------------------SE ABRE EL ARCHIVO WAV YA GUARDADO Y LO LEE EL SPEECH, LO TRANSFORMA A TEXTO-------------------------------------------
    # Crea una instancia de Recognizer
    r = RECo.Recognizer()

    # Abre el archivo de audio
    with RECo.AudioFile(NOMBRE_ARCHIVO_SALIDA) as fuente:
        # Lee el archivo de audio
        audio = r.record(fuente)

        try:
            # Usa el reconocimiento de voz de Google para transformar el audio a texto
            Texto = r.recognize_google(audio, language='es-ES') #Selecciona el idioma en paremtros, junto al audio ya capturado
            print("El audio dice: " + Texto) #Imprime el Texto ya transformado
        except RECo.UnknownValueError:
            print("Google Speech Recognition no pudo entender el audio")
        except RECo.RequestError as e:
            print("No se pudo solicitar resultados de Google Speech Recognition; {0}".format(e))
    return Texto


def Convertir_audio(Texto):
    tts = gTTS(text=Texto, lang='es')
    # Guarda el archivo de audio
    tts.save("output.mp3")
    # Reproduce el archivo de audio
    os.system('start output.mp3')



#------------------------------------------------ ALGORITMO DIJKSTRA -----------------------------------------
def dijkstra(grafo, inicio, final):
    # Inicializa las distancias, los nodos visitados y los nodos anteriores
    distancias = {nodo: float('inf') for nodo in grafo.nodos}
    anteriores = {nodo: None for nodo in grafo.nodos}
    distancias[inicio] = 0
    visitados = set()

    while True:
        # Encuentra el nodo no visitado con la distancia más corta
        nodo_actual = min((nodo for nodo in grafo.nodos if nodo not in visitados), key=lambda nodo: distancias[nodo], default=None)

        # Si todos los nodos han sido visitados o el nodo actual es inalcanzable, termina el algoritmo
        if nodo_actual is None or distancias[nodo_actual] == float('inf'):
            break

        # Actualiza las distancias de los nodos adyacentes
        for arista in grafo.aristas:
            if arista.Nodo1 == nodo_actual:
                vecino = arista.Nodo2
                peso = arista.Peso
            elif arista.Nodo2 == nodo_actual:  # Considera las aristas en la dirección opuesta
                vecino = arista.Nodo1
                peso = arista.Peso
            else:
                continue

            distancia_alternativa = distancias[nodo_actual] + peso
            if distancia_alternativa < distancias[vecino]:
                distancias[vecino] = distancia_alternativa
                anteriores[vecino] = nodo_actual

        # Marca el nodo actual como visitado
        visitados.add(nodo_actual)

    # Reconstruye la ruta más corta
    ruta = []
    nodo_actual = final
    while nodo_actual is not None:
        ruta.append(nodo_actual)
        nodo_actual = anteriores[nodo_actual]
    ruta.reverse()

    return ruta
# Aplica el algoritmo de Dijkstra al grafo



grafo = gF()

arista1 = aR("Manzana", "Pera", 2)
arista2 = aR("Pera", "Aguacate", 6)
arista3 = aR("Aguacate", "Jitomate", 4)
arista4 = aR("Aguacate", "Lechuga", 7)
arista5 = aR("Manzana", "Cebolla", 1)
arista6 = aR("Manzana", "Jitomate", 3)
arista7 = aR("Jitomate", "Tomatito", 2)
arista8 = aR("Jitomate", "Papaya", 6)
arista9 = aR("Papaya", "Ajos", 4)
arista10 = aR("Cebolla", "Calabaza", 7)
arista11 = aR("Cebolla", "Papas", 1)
arista12 = aR("Cebolla", "Lechuga", 3)


grafo.AgregarArista(arista1)
grafo.AgregarArista(arista2)
grafo.AgregarArista(arista3)
grafo.AgregarArista(arista4)
grafo.AgregarArista(arista5)
grafo.AgregarArista(arista6)
grafo.AgregarArista(arista7)
grafo.AgregarArista(arista8)
grafo.AgregarArista(arista9)
grafo.AgregarArista(arista10)
grafo.AgregarArista(arista11)
grafo.AgregarArista(arista12)

ruta = dijkstra(grafo, 'Manzana', 'Jitomate')
print(ruta)

ruta = dijkstra(grafo, 'Manzana', 'Lechuga')
print(ruta)
#print(dijkstra(grafo, "A"))
#distancias = dijkstra(grafo, 'A')

def FijarNodos():

    Convertir_audio("Dime tu nodo inicio")
    NodoInicio = Convertir_texto()
    Convertir_audio("Dime tu nodo destino")
    NodoDestino = Convertir_texto()

    return NodoInicio, NodoDestino

NodI, NodD = FijarNodos()
NodI = NodI.capitalize()
NodD = NodD.capitalize()
ruta = dijkstra(grafo, NodI, NodD)
Convertir_audio(f"El camino mas corto es: {ruta}")
