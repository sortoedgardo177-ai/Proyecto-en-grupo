import tkinter as tk
from tkinter import ttk, messagebox
import csv
from tkinter import filedialog
from Modelos.gestor_json import leer_datos
import json

class Dashboard(tk.Toplevel):
    def __init__(self, master, usuario_info):
        super().__init__(master)
        self.master = master 
        self.title("IPAM Dashboard | Gestión de Red")
        self.geometry("1100x750") 
        self.configure(bg="#f8fafc")
        
        # Guardamos la info del usuario y su rol
        self.usuario_nombre = usuario_info['usuario']
        self.rol = usuario_info['rol'].lower() # Lo pasamos a minúsculas para evitar errores

        # --- ESTILOS ---
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview", background="white", rowheight=35, font=("Arial", 10))
        style.configure("Treeview.Heading", background="#f1f5f9", font=("Arial", 10, "bold"))

        # --- HEADER ---
        header = tk.Frame(self, bg="#0f172a", height=70)
        header.pack(fill="x")
        
        self.btn_logout = tk.Button(
            header, text="↩ Cerrar Sesión", fg="white", bg="#1e293b",
            font=("Arial", 10, "bold"), relief="flat", cursor="hand2",
            activebackground="#ef4444", 
            command=self.cerrar_sesion
        )
        self.btn_logout.pack(side="left", padx=20, pady=20)

        tk.Label(header, text="SISTEMA IPAM", fg="#3b82f6", bg="#0f172a", 
                 font=("Arial", 14, "bold")).pack(side="left", padx=10)
        
        user_text = f"Sesión: {self.usuario_nombre} | Rol: {self.rol.upper()}"
        tk.Label(header, text=user_text, fg="#cbd5e1", bg="#0f172a", 
                 font=("Arial", 9)).pack(side="right", padx=30)

        # --- CONTENEDOR PRINCIPAL ---
        container = tk.Frame(self, bg="#f8fafc", padx=40, pady=10)
        container.pack(fill="both", expand=True)

        # --- 🔍 BÚSQUEDA ---
        search_frame = tk.Frame(container, bg="#f8fafc")
        search_frame.pack(fill="x", pady=(10, 20))

        tk.Label(search_frame, text="🔍 Buscar:", bg="#f8fafc", 
                 font=("Arial", 10, "bold"), fg="#64748b").pack(side="left")
        
        self.ent_buscar = tk.Entry(search_frame, font=("Arial", 10), relief="flat", 
                                   bg="white", highlightthickness=1, highlightbackground="#e2e8f0")
        self.ent_buscar.pack(side="left", padx=10, fill="x", expand=True, ipady=8)
        self.ent_buscar.bind("<KeyRelease>", lambda e: self.filtrar_datos())

        # --- TABLA (TREEVIEW) ---
        self.tabla = ttk.Treeview(container, columns=("IP", "MAC", "DISP", "DEPTO"), show="headings")
        self.tabla.heading("IP", text="DIRECCIÓN IP")
        self.tabla.heading("MAC", text="DIRECCIÓN MAC")
        self.tabla.heading("DISP", text="DISPOSITIVO")
        self.tabla.heading("DEPTO", text="DEPARTAMENTO")
        
        for col in ("IP", "MAC", "DISP", "DEPTO"):
            self.tabla.column(col, anchor="center")
        self.tabla.pack(fill="both", expand=True)

        #  BOTONERA 
        btn_container = tk.Frame(self, bg="#f8fafc", pady=25)
        btn_container.pack(fill="x")

        # 1. Botón Nuevo 
        self.btn_nuevo = tk.Button(
            btn_container, text="+ Nuevo Registro", 
            bg="#10b981", fg="white", font=("Arial", 10, "bold"),
            relief="flat", padx=20, pady=10, cursor="hand2",
            command=self.abrir_formulario
        )
        self.btn_nuevo.pack(side="left", padx=(40, 10))

        #  Botón Eliminar
        if self.rol in ["admin", "tecnico"]:
            self.btn_eliminar = tk.Button(
                btn_container, text="Eliminar Seleccionado", 
                bg="#ef4444", fg="white", font=("Arial", 10, "bold"),
                relief="flat", padx=20, pady=10, cursor="hand2",
                command=self.eliminar_dato
            )
            self.btn_eliminar.pack(side="left", padx=10)

        # 3. Botón Gestionar Usuarios
        if self.rol == "admin":
            self.btn_usuarios = tk.Button(
                btn_container, text="👥 Gestionar Usuarios", 
                bg="#6366f1", fg="white", font=("Arial", 10, "bold"),
                relief="flat", padx=20, pady=10, cursor="hand2",
                command=self.abrir_gestion_usuarios
            )
            self.btn_usuarios.pack(side="right", padx=40)

        self.cargar_datos()
        self.btn_exportar = tk.Button(
            btn_container, text="📊 Exportar CSV", 
            bg="#64748b", fg="white", font=("Arial", 10, "bold"),
            relief="flat", padx=20, pady=10, cursor="hand2",
            command=self.exportar_csv
        )
        self.btn_exportar.pack(side="left", padx=10)

    # --- FUNCIONES ---
    def cerrar_sesion(self):
        if messagebox.askyesno("Cerrar Sesión", "¿Desea salir de la cuenta actual?"):
            self.destroy() 
            self.master.deiconify() 

    def abrir_formulario(self):
        from Vistas.vista_formulario import VistaFormulario
        VistaFormulario(self, self.usuario_nombre, self.cargar_datos)

    def abrir_gestion_usuarios(self):
        try:
            from Vistas.vista_usuarios import VistaUsuarios
            VistaUsuarios(self, self.usuario_nombre)
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo abrir la gestión: {e}")

    def cargar_datos(self):
        self.filtrar_datos()

    def filtrar_datos(self):
        termino = self.ent_buscar.get().lower()
        for fila in self.tabla.get_children():
            self.tabla.delete(fila)
        
        registros = leer_datos("registros")
        for r in registros:
            ip = str(r.get('ip', '')).lower()
            disp = str(r.get('dispositivo', '')).lower()
            depto = str(r.get('departamento', '')).lower()
            
            if termino in ip or termino in disp or termino in depto:
                self.tabla.insert("", "end", values=(
                    r.get('ip', 'N/A'), r.get('mac', 'N/A'), 
                    r.get('dispositivo', 'N/A'), r.get('departamento', 'N/A')
                ))

    def eliminar_dato(self):
        seleccion = self.tabla.selection()
        if not seleccion:
            messagebox.showwarning("Atención", "Seleccione un registro de la tabla")
            return

        item = self.tabla.item(seleccion)
        ip_borrar = item['values'][0]

        if messagebox.askyesno("Confirmar", f"¿Eliminar permanentemente la IP {ip_borrar}?"):
            try:
                registros = leer_datos("registros")
                # Filtramos para quitar la IP seleccionada
                nuevos = [r for r in registros if str(r.get('ip')) != str(ip_borrar)]
                
                with open("Datos/registros.json", "w", encoding="utf-8") as f:
                    json.dump(nuevos, f, indent=4)
                
                self.cargar_datos()
                messagebox.showinfo("Éxito", f"Registro {ip_borrar} eliminado.")
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo eliminar: {e}")

    def exportar_csv(self):
        # 1. Obtener los datos actuales
        registros = leer_datos("registros")
        
        if not registros:
            messagebox.showwarning("Exportar", "No hay datos para exportar.")
            return

        # 2. Preguntar dónde
        archivo = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("Archivo CSV", "*.csv")],
            title="Guardar reporte de Red"
        )

        if archivo:
            try:
                # 3. Escribir el archivo CSV
                with open(archivo, mode='w', newline='', encoding='utf-8') as f:
                    # Definimos las columnas (Cabeceras)
                    columnas = ["ip", "mac", "dispositivo", "departamento"]
                    writer = csv.DictWriter(f, fieldnames=columnas)
                    
                    writer.writeheader() # Escribe los títulos
                    writer.writerows(registros) # Escribe todos los datos
                
                messagebox.showinfo("Éxito", f"Reporte exportado correctamente en:\n{archivo}")
            
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo exportar el archivo: {e}")