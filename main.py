import tkinter as tk
from tkinter import messagebox
import json
import os

def cargar_usuarios():
    if not os.path.exists('usuarios.txt'):
        return []
    with open('usuarios.txt', 'r') as file:
        return json.load(file)

def guardar_usuarios(usuarios):
    with open('usuarios.txt', 'w') as file:
        json.dump(usuarios, file)

def cargar_pagos():
    if not os.path.exists('pagos.txt'):
        return []
    with open('pagos.txt', 'r') as file:
        return json.load(file)

def guardar_pagos(pagos):
    with open('pagos.txt', 'w') as file:
        json.dump(pagos, file)


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
        tk.Button(self.root, text="Consultar Estado de Cuenta", command=self.consultar_estado_cuenta).grid(row=3,
                                                                                                           column=0)
        tk.Button(self.root, text="Descargar Recibo", command=self.descargar_recibo).grid(row=4, column=0)

    def mostrar_dashboard_secretario(self):
        tk.Button(self.root, text="Realizar Pago", command=self.realizar_pago).grid(row=2, column=0)
        tk.Button(self.root, text="Consultar Estado de Cuenta de Alumno",
                  command=self.consultar_estado_cuenta_alumno).grid(row=3, column=0)
        tk.Button(self.root, text="Descargar Recibo", command=self.descargar_recibo).grid(row=4, column=0)

    def limpiar_interfaz(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def logout(self):
        self.usuario_actual = None
        self.crear_interfaz_login()

    # Funciones adicionales para cada acción específica
    def gestionar_usuarios(self):
        # Implementar la lógica de gestión de usuarios aquí
        pass

    def configurar_parametros(self):
        # Implementar la lógica de configuración de parámetros aquí
        pass

    def generar_informes(self):
        # Implementar la lógica de generación de informes aquí
        pass

    def realizar_pago(self):
        # Implementar la lógica de realización de pagos aquí
        pass

    def consultar_estado_cuenta(self):
        # Implementar la lógica de consulta de estado de cuenta aquí
        pass

    def descargar_recibo(self):
        # Implementar la lógica de descarga de recibos aquí
        pass

    def consultar_estado_cuenta_alumno(self):
        # Implementar la lógica de consulta de estado de cuenta de alumno aquí
        pass

if __name__ == "__main__":
    root = tk.Tk()
    app = PaymentSystemApp(root)
    root.mainloop()

