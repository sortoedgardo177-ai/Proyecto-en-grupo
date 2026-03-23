import tkinter as tk
from tkinter import messagebox
from Modelos.gestor_json import guardar_dato
from Modelos.autenticacion import registrar_log

class VistaFormulario(tk.Toplevel):
    def __init__(self, master, usuario_actual, callback_actualizar):
        super().__init__(master)
        self.title("Registrar Nueva IP")
        self.geometry("350x450")
        self.usuario = usuario_actual
        self.callback = callback_actualizar # Función para refrescar la tabla al terminar
        
        # Color
        bg_color = "#f8fafc"
        self.configure(bg=bg_color)

        # Encabezado
        tk.Label(self, text="GESTIÓN DE RED (IPAM)", font=("Inter", 12, "bold"), bg=bg_color).pack(pady=10)

        # Atributos: IP, MAC, Dispositivo, Departamento
        self.entry_ip = self.crear_campo("Dirección IP:")
        self.entry_mac = self.crear_campo("Dirección MAC:")
        self.entry_disp = self.crear_campo("Dispositivo (PC/Router):")
        self.entry_depto = self.crear_campo("Departamento:")

        # Botón para Guardar 
        tk.Button(
            self, 
            text="GUARDAR REGISTRO", 
            command=self.validar_y_enviar,
            bg="#10b981", # Verde institucional
            fg="white", 
            font=("Inter", 10, "bold"),
            padx=20,
            pady=10
        ).pack(pady=20)

    def crear_campo(self, texto):
        """Crea una etiqueta y un campo de entrada."""
        tk.Label(self, text=texto, bg="#f8fafc", fg="#1e293b").pack(pady=(10, 0))
        entry = tk.Entry(self, width=30)
        entry.pack(pady=5)
        return entry

    def validar_y_enviar(self):
        # 1. Recopilar datos del formulario
        datos_ipam = {
            "ip": self.entry_ip.get(),
            "mac": self.entry_mac.get(),
            "dispositivo": self.entry_disp.get(),
            "departamento": self.entry_depto.get()
        }

        # 2. Validación básica (Rol del Analista QA)
        if not datos_ipam["ip"] or not datos_ipam["mac"]:
            messagebox.showwarning("Campos Vacíos", "Los campos IP y MAC son obligatorios.")
            return

        # 3. guardar en registros.json 
        exito, mensaje = guardar_dato("registros", datos_ipam)

        if exito:
            # 4. Registrar la acción en el log
            registrar_log(self.usuario, f"Registró exitosamente la IP: {datos_ipam['ip']}")
            messagebox.showinfo("Éxito", "Dispositivo registrado correctamente.")
            self.callback() # Refresca el Treeview en vista_dashboard.py
            self.destroy()  # Cierra la ventana del formulario
        else:
            messagebox.showerror("Error de Duplicado", mensaje)