import os
import pickle

def escanear_discos():
    discos = []
    for disco in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
        ruta_disco = f"{disco}:\\"
        if os.path.exists(ruta_disco):
            discos.append(ruta_disco)
    return discos

def buscar_archivo(archivo, discos, cache):
    if os.path.exists(cache):
        with open(cache, 'rb') as f:
            resultados_cache = pickle.load(f)
            for disco, archivos_en_disco in resultados_cache.items():
                if archivo in archivos_en_disco:
                    print(f"¡Archivo encontrado en el disco {disco} (según el caché)!")
                    return

    resultados = {}
    for disco in discos:
        archivos_en_disco = []
        for carpeta_actual, carpetas, archivos in os.walk(disco):
            if archivo in archivos:
                ruta_completa = os.path.join(carpeta_actual, archivo)
                archivos_en_disco.append(ruta_completa)
                print(f"¡Archivo encontrado en {ruta_completa}!")
        resultados[disco] = archivos_en_disco

    with open(cache, 'wb') as f:
        pickle.dump(resultados, f)
        print("Caché actualizado.")

archivo_a_buscar = input("Ingrese el nombre del archivo a buscar: ")
discos_disponibles = escanear_discos()
    
if not discos_disponibles:
        print("No se encontraron discos disponibles.")
else:
    cache_file = "cache_resultados.pkl"
    if not os.path.exists(cache_file):
        print("Realizando el escaneo inicial y caché...")
        buscar_archivo(archivo_a_buscar, discos_disponibles, cache_file)
    else:
        buscar_archivo(archivo_a_buscar, discos_disponibles, cache_file)
