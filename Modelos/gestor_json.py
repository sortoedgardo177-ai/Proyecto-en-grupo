import json
import os

def leer_datos(archivo):
    """Lee datos de la carpeta datos/ (crea la carpeta si no existe)"""
    if not os.path.exists("datos"):
        os.makedirs("datos")
        
    ruta = f"datos/{archivo}.json"
    try:
        with open(ruta, "r", encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def guardar_dato(archivo, nuevo_dato):
    ruta = f"Datos/{archivo}.json"
    datos = leer_datos(archivo)
    
    # Validación de duplicados para registros 
    campo_id = "ip" if archivo == "registros" else "usuario"
    
    for item in datos:
        if item.get(campo_id) == nuevo_dato.get(campo_id):
            return False, f"Ese {campo_id} ya existe en el sistema."

    datos.append(nuevo_dato)
    
    try:
        with open(ruta, "w", encoding="utf-8") as f:
            json.dump(datos, f, indent=4)
        return True, "Guardado exitosamente."
    except Exception as e:
        return False, str(e)