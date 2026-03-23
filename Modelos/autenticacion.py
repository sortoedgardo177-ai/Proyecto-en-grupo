import datetime
from Modelos.gestor_json import leer_datos

from Modelos.gestor_json import leer_datos

def validar_usuario(user, password):
    usuarios = leer_datos("usuarios")
    for u in usuarios:
        db_user = str(u.get('usuario', '')).strip().lower()
        input_user = str(user).strip().lower()
        
        # Buscamos 'clave' o 'password' para evitar el KeyError
        db_clave = str(u.get('clave') or u.get('password', '')).strip()
        input_clave = str(password).strip()

        if db_user == input_user and db_clave == input_clave:
            return u
    return None
def registrar_log(usuario, accion):
    fecha = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open("datos/auditoria.log", "a") as f:
        f.write(f"{fecha} | {usuario} | {accion}\n") 