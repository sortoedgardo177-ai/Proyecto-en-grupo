import tkinter as tk
from tkinter import ttk, messagebox
from Modelos.gestor_json import leer_datos, guardar_dato
import json

class VistaUsuarios(tk.Toplevel):
    def __init__(self, master, usuario_nombre):
        super().__init__(master)
        self.title("Gestión de Usuarios y Técnicos")
        self.geometry("950x550") # Ancho ajustado para la tabla
        self.configure(bg="#f8fafc")
        
        # Guardamos el nombre del admin actual para evitar que se borre a sí mismo
        self.usuario_nombre = usuario_nombre

        # --- PANEL IZQUIERDO: FORMULARIO DE REGISTRO ---
        frame_form = tk.Frame(self, bg="white", padx=25, pady=25, highlightthickness=1, highlightbackground="#e2e8f0")
        frame_form.pack(side="left", fill="y", padx=20, pady=20)

        tk.Label(frame_form, text="REGISTRAR USUARIO", font=("Arial", 11, "bold"), bg="white", fg="#0f172a").pack(pady=(0, 20))

        self.ent_user = self.crear_campo(frame_form, "Nombre de Usuario")
        self.ent_pass = self.crear_campo(frame_form, "Contraseña (PIN)")
        
        tk.Label(frame_form, text="Rol del Usuario:", bg="white", font=("Arial", 9), fg="#64748b").pack(anchor="w", padx=20)
        self.combo_rol = ttk.Combobox(frame_form, values=["tecnico", "admin"], state="readonly")
        self.combo_rol.set("tecnico")
        self.combo_rol.pack(pady=5, padx=20, fill="x")

        tk.Button(
            frame_form, text="💾 GUARDAR USUARIO", bg="#10b981", fg="white", 
            font=("Arial", 10, "bold"), relief="flat", pady=10, cursor="hand2",
            command=self.registrar_usuario
        ).pack(fill="x", padx=20, pady=25)

        # --- PANEL DERECHO: VISOR DE USUARIOS ---
        frame_visor = tk.Frame(self, bg="#f8fafc", padx=10, pady=20)
        frame_visor.pack(side="right", fill="both", expand=True)

        tk.Label(frame_visor, text="USUARIOS ACTIVOS", font=("Arial", 11, "bold"), bg="#f8fafc", fg="#0f172a").pack(pady=(0, 15))

        # Configuración de la Tabla (Treeview)
        self.tabla_user = ttk.Treeview(frame_visor, columns=("USER", "ROL"), show="headings")
        self.tabla_user.heading("USER", text="NOMBRE DE USUARIO")
        self.tabla_user.heading("ROL", text="ROL")
        self.tabla_user.column("USER", anchor="center", width=150)
        self.tabla_user.column("ROL", anchor="center", width=100)
        self.tabla_user.pack(fill="both", expand=True, padx=10)

        # Botón Eliminar
        tk.Button(
            frame_visor, text="🗑️ ELIMINAR SELECCIONADO", bg="#ef4444", fg="white", 
            font=("Arial", 9, "bold"), relief="flat", pady=8, cursor="hand2",
            command=self.eliminar_usuario
        ).pack(pady=15)

        # Cargar los datos al iniciar
        self.actualizar_tabla()

    def crear_campo(self, parent, texto):
        tk.Label(parent, text=texto, bg="white", font=("Arial", 9), fg="#64748b").pack(anchor="w", padx=20)
        entry = tk.Entry(parent, font=("Arial", 10), bg="#f1f5f9", relief="flat")
        entry.pack(fill="x", padx=20, pady=5, ipady=6)
        return entry

    def actualizar_tabla(self):
        """Recarga la lista de usuarios desde el archivo JSON"""
        for item in self.tabla_user.get_children():
            self.tabla_user.delete(item)
        
        usuarios = leer_datos("usuarios")
        for u in usuarios:
            self.tabla_user.insert("", "end", values=(u.get('usuario'), u.get('rol')))

    def registrar_usuario(self):
        u = self.ent_user.get().strip()
        p = self.ent_pass.get().strip()
        r = self.combo_rol.get()

        if not u or not p:
            messagebox.showwarning("Atención", "Completa todos los campos")
            return

        nuevo_user = {"usuario": u, "clave": p, "rol": r}
        exito, msg = guardar_dato("usuarios", nuevo_user)
        
        if exito:
            messagebox.showinfo("Éxito", f"Usuario {u} creado")
            self.ent_user.delete(0, tk.END)
            self.ent_pass.delete(0, tk.END)
            self.actualizar_tabla()
        else:
            messagebox.showerror("Error", msg)

    def eliminar_usuario(self):
        seleccion = self.tabla_user.selection()
        if not seleccion:
            messagebox.showwarning("Atención", "Selecciona un usuario de la lista")
            return

        item = self.tabla_user.item(seleccion)
        nombre_a_borrar = item['values'][0]

        # SEGURIDAD: Evitar que el admin se borre a sí mismo
        if nombre_a_borrar == self.usuario_nombre:
            messagebox.showerror("Error", "No puedes eliminar tu propia cuenta administrativa.")
            return

        if messagebox.askyesno("Confirmar", f"¿Eliminar al usuario '{nombre_a_borrar}'?"):
            try:
                usuarios = leer_datos("usuarios")
                nueva_lista = [u for u in usuarios if u.get('usuario') != nombre_a_borrar]
                
                with open("Datos/usuarios.json", "w", encoding="utf-8") as f:
                    json.dump(nueva_lista, f, indent=4)
                
                self.actualizar_tabla()
                messagebox.showinfo("Éxito", f"Usuario '{nombre_a_borrar}' eliminado.")
            except Exception as e:
                messagebox.showerror("Error", f"Fallo al eliminar: {e}")