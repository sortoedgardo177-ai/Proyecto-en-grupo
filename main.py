import tkinter as tk
from tkinter import messagebox
from Modelos.autenticacion import validar_usuario
from Vistas.vista_dashboard import Dashboard

def intentar_login():
    user = entry_user.get()
    pw = entry_pw.get()
    
    resultado = validar_usuario(user, pw)
    
    if resultado:
    
        root.withdraw() 
        
        #  Abrimos el Dashboard pasando 'root' como el master
        Dashboard(root, resultado) 
    else:
        messagebox.showerror("Error", "Credenciales incorrectas")

root = tk.Tk()
root.title("Login IPAM")
root.geometry("300x250")

tk.Label(root, text="Usuario:").pack(pady=5)
entry_user = tk.Entry(root)
entry_user.pack()

tk.Label(root, text="Clave:").pack(pady=5)
entry_pw = tk.Entry(root, show="*")
entry_pw.pack()

tk.Button(root, text="Entrar", command=intentar_login).pack(pady=20)

root.mainloop()