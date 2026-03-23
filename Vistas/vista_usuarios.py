import tkinter as tk
from tkinter import ttk, messagebox # Añadí ttk por el Combobox
from Modelos.gestor_json import leer_datos, guardar_dato

class VistaUsuarios(tk.Toplevel):
    # AGREGADO: 'usuario_nombre' para recibir el dato que viene del Dashboard
    def __init__(self, master, usuario_nombre): 
        super().__init__(master)
        
        # Guardamos el nombre por si quieres mostrarlo en algún Label después
        self.admin_que_registra = usuario_nombre 
        
        self.title("Gestión de Técnicos")
        self.geometry("400x450")
        self.configure(bg="white")

        tk.Label(self, text="REGISTRAR NUEVO USUARIO", font=("Arial", 12, "bold"), bg="white", pady=20).pack()

        # Campos
        self.ent_user = self.crear_campo("Nombre de Usuario")
        self.ent_pass = self.crear_campo("Contraseña (PIN)")
        
        tk.Label(self, text="Rol del Usuario:", bg="white", font=("Arial", 9)).pack(pady=(10,0))
        
        # Uso de ttk para el Combobox
        self.combo_rol = ttk.Combobox(self, values=["tecnico", "admin"], state="readonly")
        self.combo_rol.set("tecnico")
        self.combo_rol.pack(pady=5, padx=40, fill="x")

        tk.Button(self, text="CREAR USUARIO", bg="#3b82f6", fg="white", font=("Arial", 10, "bold"),
                  relief="flat", pady=10, command=self.registrar_usuario).pack(fill="x", padx=40, pady=30)

    def crear_campo(self, texto):
        tk.Label(self, text=texto, bg="white", font=("Arial", 9), fg="#64748b").pack(anchor="w", padx=40)
        entry = tk.Entry(self, font=("Arial", 11), bg="#f1f5f9", relief="flat")
        entry.pack(fill="x", padx=40, pady=5, ipady=8)
        return entry

    def registrar_usuario(self):
        u = self.ent_user.get()
        p = self.ent_pass.get()
        r = self.combo_rol.get()

        if not u or not p:
            messagebox.showwarning("Atención", "Todos los campos son obligatorios")
            return

        # Estructura para usuarios.json
        nuevo_user = {"usuario": u, "clave": p, "rol": r}
        
        # Guardar en usuarios.json usando tu gestor
        exito, msg = guardar_dato("usuarios", nuevo_user)
        if exito:
            messagebox.showinfo("Éxito", f"Usuario {u} creado correctamente")
            self.destroy()
        else:
            messagebox.showerror("Error", msg)