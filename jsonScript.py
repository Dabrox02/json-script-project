import os
import json

def generar_json_directorio(folder):
    ruta = f"{os.getcwd()}{folder}"

    directorio = {
    }

    for item in sorted(os.listdir(ruta)):
        item_path = os.path.join(ruta, item)
        if os.path.isdir(item_path):
            directorio[item] = {
                "sectionName":"",
                "videos": [],
            }
            
            if len(os.listdir(item_path)) > 0:
                for archivo in sorted(os.listdir(item_path)):
                    if os.path.isdir(f"{item_path}/{archivo}"):
                        if(archivo == "videos"):
                            for i, video in enumerate(os.listdir(f"{item_path}/{archivo}")):
                                directorio[item]["videos"].append(
                                    {
                                        i+1: {
                                            "titulo": "",
                                            "video": video,
                                            "links": {}
                                        }
                                    }
                                )
    return directorio

directorio = generar_json_directorio("/git")
with open("estructura.json", "w") as json_file:
     json.dump(directorio, json_file, indent=4)

