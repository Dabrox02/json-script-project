import os
import json

def crear_section_config(ubicacion):
    section_config = {
        "sectionName": "",
        "videos": []
    }
    
    videos_dir = os.path.join(ubicacion, 'videos')

    if os.path.exists(videos_dir) and os.path.isdir(videos_dir):
        video_files = sorted(os.listdir(videos_dir))
        for i, video_file in enumerate(video_files, start=1):
            video = {
                f"{i}": {
                    "titulo": "",
                    "texto": [],
                    "links": []
                }
            }
            section_config["videos"].append(video)

    with open(os.path.join(ubicacion, 'sectionConfig.json'), 'w') as json_file:
        json.dump(section_config, json_file, indent=4)

# def recorrer_crear_section_config(folder):
#     ruta = f"{os.getcwd()}{folder}"
#     for subcarpeta in sorted(os.listdir(ruta)):
#         subcarpeta_path = os.path.join(ruta, subcarpeta)
#         if os.path.isdir(subcarpeta_path):
#             crear_section_config(subcarpeta_path)

def recorrer_crear_section_config(folder):
    ruta = f"{os.getcwd()}{folder}"
    for subcarpeta in sorted(os.listdir(ruta)):
        subcarpeta_path = os.path.join(ruta, subcarpeta)
        if os.path.isdir(subcarpeta_path):
            section_config_path = os.path.join(subcarpeta_path, 'sectionConfig.json')
            if not os.path.exists(section_config_path):
                crear_section_config(subcarpeta_path)

def list_file_folder(ruta):
    archivos = []
    carpetas = []
    
    for item in sorted(os.listdir(ruta)):
        item_path = os.path.join(ruta, item)
        if os.path.isdir(item_path):
            carpetas.append(item)
        else:
            archivos.append(item)
    return archivos, carpetas

def leer_archivos_section(ruta):
    section_config_path = os.path.join(ruta, 'sectionConfig.json')
    try:
        with open(section_config_path, "r") as archivo:
            datos = json.load(archivo)
            return datos
    except FileNotFoundError:
        print(f"El archivo '{section_config_path}' no se encontró.")
    except json.JSONDecodeError as e:
        print(f"Error al decodificar el archivo JSON: {e}")
    except Exception as e:
        print(f"Ocurrió un error inesperado: {e}")

def procesar_directorio(folder):
    ruta = f"{os.getcwd()}{folder}"
    directorio = {}
    archivos, carpetas = list_file_folder(ruta)

    for carpeta in carpetas:
        carpeta_path = os.path.join(ruta, carpeta)
        section_config = leer_archivos_section(carpeta_path)
              
        directorio[carpeta] = {
            "sectionName": section_config["sectionName"] if section_config["sectionName"] else "No name",
            "videos": [],
        }

        archivos_en_carpeta, subcarpetas = list_file_folder(carpeta_path)

        if archivos_en_carpeta:
            for archivo in sorted(archivos_en_carpeta):
                archivo_path = os.path.join(carpeta_path, archivo)

        for subcarpeta in subcarpetas:
            subcarpeta_path = os.path.join(carpeta_path, subcarpeta)

            if subcarpeta == "videos":
                for i, video in enumerate(sorted(os.listdir(subcarpeta_path))):
                    video_conf = section_config["videos"][i][f"{i+1}"]
                    directorio[carpeta]["videos"].append({
                        f"{i+1}": {
                            "titulo": video_conf["titulo"],
                            "video": video,
                            "links": []
                        }
                    })
                    if not video_conf["texto"] == []: 
                        directorio[carpeta]["videos"][i][f"{i+1}"]["texto"] = video_conf["texto"]
                    if not video_conf["links"] == []: 
                        directorio[carpeta]["videos"][i][f"{i+1}"]["links"] = video_conf["links"]
    return directorio


def main():
    folder = input("Ingrese nombre de la carpeta: ").strip()
    ruta = f"/{folder}"
    recorrer_crear_section_config(ruta)
    directorio = procesar_directorio(ruta)

    with open("estructura.json", "w") as json_file:
        json.dump(directorio, json_file, indent=4)

main()