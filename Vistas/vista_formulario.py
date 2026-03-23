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
        
        # Colores 
        bg_color = "#f8fafc"
        self.configure(bg=bg_color)

        # Título
        tk.Label(self, text="GESTIÓN DE DIRECCIONES", font=("Inter", 12, "bold"), bg=bg_color).pack(pady=10)

        # Campos de entrada (Atributos IPAM)
        self.entry_ip = self.crear_campo("Dirección IP (ej: 192.168.1.50)")
        self.entry_mac = self.crear_campo("Dirección MAC (ej: 00:1A:2B...)")
        self.entry_disp = self.crear_campo("Nombre del Dispositivo")
        self.entry_depto = self.crear_campo("Departamento / Ubicación")

        # Botón Guardar
        tk.Button(
            self, 
            text="GUARDAR REGISTRO", 
            command=self.validar_y_enviar,
            bg="#10b981", 
            fg="white", 
            font=("Inter", 10, "bold"),
            padx=20,
            pady=10
        ).pack(pady=20)

    def crear_campo(self, texto):
        tk.Label(self, text=texto, bg="#f8fafc", fg="#1e293b").pack(pady=(10, 0))
        entry = tk.Entry(self, width=30)
        entry.pack(pady=5)
        return entry

    def validar_y_enviar(self):
        # 1. Obtener datos
        nueva_ip = {
            "ip": self.entry_ip.get(),
            "mac": self.entry_mac.get(),
            "dispositivo": self.entry_disp.get(),
            "departamento": self.entry_depto.get()
        }

        # 2. Validación simple (QA)
        if not nueva_ip["ip"] or not nueva_ip["mac"]:
            messagebox.showwarning("Atención", "IP y MAC son campos obligatorios.")
            return

        # 3. Intentar guardar en registros.json
        exito, mensaje = guardar_dato("registros", nueva_ip)

        if exito:
            # 4. Registrar en auditoria.log (Fase 2, Paso 4)
            registrar_log(self.usuario, f"Registró nueva IP: {nueva_ip['ip']}")
            messagebox.showinfo("Éxito", mensaje)
            self.callback() # Refresca el Treeview en el Dashboard
            self.destroy()  # Cierra el formulario
        else:
            messagebox.showerror("Error", mensaje)