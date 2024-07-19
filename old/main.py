import tkinter as tk
from tkinter import messagebox
import json
import os

# Funciones auxiliares para manejo de archivos
def cargar_usuarios():
    if not os.path.exists('../usuarios.txt'):
        return []
    with open('../old_v2/usuarios.txt', 'r') as file:
        try:
            return json.load(file)
        except json.JSONDecodeError:
            return []

def guardar_usuarios(usuarios):
    with open('../old_v2/usuarios.txt', 'w') as file:
        json.dump(usuarios, file)

def cargar_pagos():
    if not os.path.exists('pagos.txt'):
        return []
    with open('pagos.txt', 'r') as file:
        try:
            return json.load(file)
        except json.JSONDecodeError:
            return []

def guardar_pagos(pagos):
    with open('pagos.txt', 'w') as file:
        json.dump(pagos, file)

# Clase principal de la aplicación
class PaymentSystemApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema de Pagos del Colegio")

        self.usuarios = cargar_usuarios()
        self.pagos = cargar_pagos()
        self.usuario_actual = None

        self.crear_interfaz_login()

    def crear_interfaz_login(self):
        self.limpiar_interfaz()

        tk.Label(self.root, text="Email").grid(row=0, column=0)
        tk.Label(self.root, text="Password").grid(row=1, column=0)

        self.email = tk.Entry(self.root)
        self.password = tk.Entry(self.root, show="*")

        self.email.grid(row=0, column=1)
        self.password.grid(row=1, column=1)

        tk.Button(self.root, text="Login", command=self.login).grid(row=2, column=1)

    def login(self):
        email = self.email.get()
        password = self.password.get()

        for usuario in self.usuarios:
            if usuario['email'] == email and usuario['password'] == password:
                self.usuario_actual = usuario
                self.mostrar_dashboard()
                return

        messagebox.showerror("Error", "Credenciales incorrectas")

    def mostrar_dashboard(self):
        self.limpiar_interfaz()

        tk.Label(self.root, text=f"Bienvenido {self.usuario_actual['email']}").grid(row=0, column=0)

        if self.usuario_actual['rol'] == 'admin':
            self.mostrar_dashboard_admin()
        elif self.usuario_actual['rol'] in ['alumno', 'apoderado']:
            self.mostrar_dashboard_alumno()
        elif self.usuario_actual['rol'] == 'secretario':
            self.mostrar_dashboard_secretario()

        tk.Button(self.root, text="Logout", command=self.logout).grid(row=1, column=0)

    def mostrar_dashboard_admin(self):
        tk.Button(self.root, text="Gestionar Usuarios", command=self.gestionar_usuarios).grid(row=2, column=0)
        tk.Button(self.root, text="Configurar Parámetros", command=self.configurar_parametros).grid(row=3, column=0)
        tk.Button(self.root, text="Generar Informes", command=self.generar_informes).grid(row=4, column=0)

    def mostrar_dashboard_alumno(self):
        tk.Button(self.root, text="Realizar Pago", command=self.realizar_pago).grid(row=2, column=0)
        tk.Button(self.root, text="Consultar Estado de Cuenta", command=self.consultar_estado_cuenta).grid(row=3, column=0)
        tk.Button(self.root, text="Descargar Recibo", command=self.descargar_recibo).grid(row=4, column=0)

    def mostrar_dashboard_secretario(self):
        tk.Button(self.root, text="Realizar Pago", command=self.realizar_pago).grid(row=2, column=0)
        tk.Button(self.root, text="Consultar Estado de Cuenta de Alumno", command=self.consultar_estado_cuenta_alumno).grid(row=3, column=0)
        tk.Button(self.root, text="Descargar Recibo", command=self.descargar_recibo).grid(row=4, column=0)

    def limpiar_interfaz(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def logout(self):
        self.usuario_actual = None
        self.crear_interfaz_login()

    def gestionar_usuarios(self):
        self.limpiar_interfaz()
        tk.Label(self.root, text="Gestionar Usuarios").grid(row=0, column=0)

        tk.Button(self.root, text="Agregar Usuario", command=self.agregar_usuario).grid(row=1, column=0)
        tk.Button(self.root, text="Eliminar Usuario", command=self.eliminar_usuario).grid(row=2, column=0)
        tk.Button(self.root, text="Volver", command=self.mostrar_dashboard).grid(row=3, column=0)

    def agregar_usuario(self):
        self.limpiar_interfaz()

        tk.Label(self.root, text="Email").grid(row=0, column=0)
        tk.Label(self.root, text="Password").grid(row=1, column=0)
        tk.Label(self.root, text="Rol").grid(row=2, column=0)

        self.email = tk.Entry(self.root)
        self.password = tk.Entry(self.root, show="*")

        self.email.grid(row=0, column=1)
        self.password.grid(row=1, column=1)

        self.rol = tk.StringVar(value="alumno")
        roles = ["admin", "alumno", "apoderado", "secretario"]
        for idx, rol in enumerate(roles):
            tk.Radiobutton(self.root, text=rol.capitalize(), variable=self.rol, value=rol).grid(row=2, column=1 + idx)

        tk.Button(self.root, text="Agregar", command=self.guardar_usuario).grid(row=3, column=1)
        tk.Button(self.root, text="Cancelar", command=self.gestionar_usuarios).grid(row=3, column=0)

    def guardar_usuario(self):
        nuevo_usuario = {
            'email': self.email.get(),
            'password': self.password.get(),
            'rol': self.rol.get()
        }
        self.usuarios.append(nuevo_usuario)
        guardar_usuarios(self.usuarios)
        messagebox.showinfo("Éxito", "Usuario agregado exitosamente")
        self.gestionar_usuarios()

    def eliminar_usuario(self):
        self.limpiar_interfaz()

        tk.Label(self.root, text="Email del Usuario a Eliminar").grid(row=0, column=0)
        self.email = tk.Entry(self.root)
        self.email.grid(row=0, column=1)

        tk.Button(self.root, text="Eliminar", command=self.confirmar_eliminar_usuario).grid(row=1, column=1)
        tk.Button(self.root, text="Cancelar", command=self.gestionar_usuarios).grid(row=1, column=0)

    def confirmar_eliminar_usuario(self):
        email = self.email.get()
        self.usuarios = [u for u in self.usuarios if u['email'] != email]
        guardar_usuarios(self.usuarios)
        messagebox.showinfo("Éxito", "Usuario eliminado exitosamente")
        self.gestionar_usuarios()

    def configurar_parametros(self):
        # Implementar la lógica de configuración de parámetros aquí
        pass

    def generar_informes(self):
        # Implementar la lógica de generación de informes aquí
        pass

    def realizar_pago(self):
        self.limpiar_interfaz()

        tk.Label(self.root, text="Monto").grid(row=0, column=0)
        self.monto = tk.Entry(self.root)
        self.monto.grid(row=0, column=1)

        tk.Button(self.root, text="Realizar Pago", command=self.procesar_pago).grid(row=1, column=1)
        tk.Button(self.root, text="Cancelar", command=self.mostrar_dashboard).grid(row=1, column=0)

    def procesar_pago(self):
        nuevo_pago = {
            'monto': self.monto.get(),
            'email': self.usuario_actual['email']
        }
        self.pagos.append(nuevo_pago)
        guardar_pagos(self.pagos)
        messagebox.showinfo("Éxito", "Pago realizado exitosamente")
        self.mostrar_dashboard()

    def consultar_estado_cuenta(self):
        self.limpiar_interfaz()

        tk.Label(self.root, text="Pagos Realizados").grid(row=0, column=0)
        pagos_usuario = [p for p in self.pagos if p['email'] == self.usuario_actual['email']]

        for idx, pago in enumerate(pagos_usuario, start=1):
            tk.Label(self.root, text=f"{idx}. Monto: {pago['monto']}").grid(row=idx, column=0)

        tk.Button(self.root, text="Volver", command=self.mostrar_dashboard).grid(row=len(pagos_usuario) + 1, column=0)

    def consultar_estado_cuenta_alumno(self):
        self.limpiar_interfaz()

        tk.Label(self.root, text="Email del Alumno").grid(row=0, column=0)
        self.email = tk.Entry(self.root)
        self.email.grid(row=0, column=1)

        tk.Button(self.root, text="Consultar", command=self.mostrar_estado_cuenta_alumno).grid(row=1, column=1)
        tk.Button(self.root, text="Cancelar", command=self.mostrar_dashboard_secretario).grid(row=1, column=0)

    def mostrar_estado_cuenta_alumno(self):
        email = self.email.get()
        pagos_usuario = [p for p in self.pagos if p['email'] == email]

        self.limpiar_interfaz()

        tk.Label(self.root, text=f"Pagos Realizados por {email}").grid(row=0, column=0)

        for idx, pago in enumerate(pagos_usuario, start=1):
            tk.Label(self.root, text=f"{idx}. Monto: {pago['monto']}").grid(row=idx, column=0)

        tk.Button(self.root, text="Volver", command=self.mostrar_dashboard_secretario).grid(row=len(pagos_usuario) + 1, column=0)

    def descargar_recibo(self):
        # Implementar la lógica de descarga de recibo aquí
        pass

if __name__ == "__main__":
    root = tk.Tk()
    app = PaymentSystemApp(root)
    root.mainloop()
