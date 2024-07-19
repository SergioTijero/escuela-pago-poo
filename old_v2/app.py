import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
from datetime import datetime

# Funciones auxiliares para manejo de archivos
def cargar_usuarios():
    if not os.path.exists('usuarios.txt'):
        return []
    with open('usuarios.txt', 'r') as file:
        try:
            return json.load(file)
        except json.JSONDecodeError:
            return []

def guardar_usuarios(usuarios):
    with open('usuarios.txt', 'w') as file:
        json.dump(usuarios, file)

def cargar_alumnos():
    if not os.path.exists('alumnos.txt'):
        return []
    with open('alumnos.txt', 'r') as file:
        try:
            return json.load(file)
        except json.JSONDecodeError:
            return []

def guardar_alumnos(alumnos):
    with open('alumnos.txt', 'w') as file:
        json.dump(alumnos, file)
    file.close()

def cargar_pagos():
    if not os.path.exists('old/pagos.txt'):
        return []
    with open('../old/pagos.txt', 'r') as file:
        try:
            return json.load(file)
        except json.JSONDecodeError:
            return []

def guardar_pagos(pagos):
    with open('../old/pagos.txt', 'w') as file:
        json.dump(pagos, file)

class LoginApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema de Pagos del Colegio")
        self.root.geometry("400x300")
        self.root.resizable(False, False)

        self.usuarios = cargar_usuarios()

        self.crear_interfaz_login()

    def crear_interfaz_login(self):
        self.limpiar_interfaz()

        frame = tk.Frame(self.root, padx=20, pady=20)
        frame.pack(expand=True)

        tk.Label(frame, text="Inicio de Sesión", font=("Arial", 16)).grid(row=0, column=0, columnspan=2, pady=(0, 20))
        tk.Label(frame, text="Email", font=("Arial", 12)).grid(row=1, column=0, pady=(0, 10), sticky="e")
        tk.Label(frame, text="Password", font=("Arial", 12)).grid(row=2, column=0, pady=(0, 10), sticky="e")

        self.email = tk.Entry(frame, font=("Arial", 12))
        self.password = tk.Entry(frame, show="*", font=("Arial", 12))

        self.email.grid(row=1, column=1, pady=(0, 10))
        self.password.grid(row=2, column=1, pady=(0, 10))

        tk.Button(frame, text="Login", command=self.login, font=("Arial", 12)).grid(row=3, column=0, columnspan=2, pady=(20, 0))

    def login(self):
        email = self.email.get()
        password = self.password.get()

        for usuario in self.usuarios:
            if usuario['email'] == email and usuario['password'] == password:
                if usuario['rol'] == 'admin':
                    messagebox.showinfo("Éxito", f"Bienvenido {usuario['email']}")
                    self.abrir_dashboard_admin()
                elif usuario['rol'] == 'secretario':
                    messagebox.showinfo("Éxito", f"Bienvenido {usuario['email']}")
                    self.abrir_dashboard_secretario()
                else:
                    messagebox.showinfo("Éxito", f"Bienvenido {usuario['email']}, pero no tienes acceso al dashboard")
                return

        messagebox.showerror("Error", "Credenciales incorrectas")

    def abrir_dashboard_admin(self):
        self.root.withdraw()
        dashboard = tk.Toplevel(self.root)
        DashboardAdminApp(dashboard)

    def abrir_dashboard_secretario(self):
        self.root.withdraw()
        dashboard = tk.Toplevel(self.root)
        DashboardSecretarioApp(dashboard)

    def limpiar_interfaz(self):
        for widget in self.root.winfo_children():
            widget.destroy()

class DashboardAdminApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Dashboard del Administrador")
        self.root.geometry("850x500")
        self.root.resizable(False, False)

        self.alumnos = cargar_alumnos()
        self.pagos = cargar_pagos()

        self.crear_interfaz_dashboard()

    def crear_interfaz_dashboard(self):
        notebook = ttk.Notebook(self.root)

        # Pestaña Alumnos
        self.pestana_alumnos = tk.Frame(notebook)
        notebook.add(self.pestana_alumnos, text="Alumnos")
        self.crear_pestana_alumnos()

        # Pestaña Pagos
        self.pestana_pagos = tk.Frame(notebook)
        notebook.add(self.pestana_pagos, text="Pagos")
        self.crear_pestana_pagos()

        notebook.pack(expand=True, fill='both')

    def crear_pestana_alumnos(self):
        frame = tk.Frame(self.pestana_alumnos, padx=20, pady=20)
        frame.pack(expand=True, fill='both')

        # Formulario de creación/edición de alumnos
        tk.Label(frame, text="ID Alumno", font=("Arial", 12)).grid(row=0, column=0, pady=(0, 10), sticky="e")
        tk.Label(frame, text="Nombre", font=("Arial", 12)).grid(row=1, column=0, pady=(0, 10), sticky="e")
        tk.Label(frame, text="Apellido", font=("Arial", 12)).grid(row=2, column=0, pady=(0, 10), sticky="e")
        tk.Label(frame, text="Correo", font=("Arial", 12)).grid(row=3, column=0, pady=(0, 10), sticky="e")

        self.id_alumno = tk.Entry(frame, font=("Arial", 12))
        self.nombre = tk.Entry(frame, font=("Arial", 12))
        self.apellido = tk.Entry(frame, font=("Arial", 12))
        self.correo = tk.Entry(frame, font=("Arial", 12))

        self.id_alumno.grid(row=0, column=1, pady=(0, 10))
        self.nombre.grid(row=1, column=1, pady=(0, 10))
        self.apellido.grid(row=2, column=1, pady=(0, 10))
        self.correo.grid(row=3, column=1, pady=(0, 10))

        tk.Button(frame, text="Crear Alumno", command=self.crear_alumno, font=("Arial", 12)).grid(row=4, column=0, columnspan=2, pady=(20, 0))
        tk.Button(frame, text="Editar Alumno", command=self.editar_alumno, font=("Arial", 12)).grid(row=5, column=0, columnspan=2, pady=(10, 0))
        tk.Button(frame, text="Eliminar Alumno", command=self.eliminar_alumno, font=("Arial", 12)).grid(row=6, column=0, columnspan=2, pady=(10, 0))

        # Lista de alumnos
        self.lista_alumnos = ttk.Treeview(frame, columns=("ID Alumno", "Nombre", "Apellido", "Correo"), show='headings')
        self.lista_alumnos.heading("ID Alumno", text="ID")
        self.lista_alumnos.heading("Nombre", text="Nombre")
        self.lista_alumnos.heading("Apellido", text="Apellido")
        self.lista_alumnos.heading("Correo", text="Correo")
        self.lista_alumnos.grid(row=7, column=0, columnspan=2, pady=(20, 0), sticky='nsew')

        frame.rowconfigure(7, weight=1)
        frame.columnconfigure(1, weight=1)

        self.cargar_lista_alumnos()

    def crear_pestana_pagos(self):
        frame = tk.Frame(self.pestana_pagos, padx=20, pady=20)
        frame.pack(expand=True, fill='both')

        # Formulario de registro/edición de pagos
        tk.Label(frame, text="ID Pago", font=("Arial", 12)).grid(row=0, column=0, pady=(0, 10), sticky="e")
        tk.Label(frame, text="ID Alumno", font=("Arial", 12)).grid(row=1, column=0, pady=(0, 10), sticky="e")
        tk.Label(frame, text="Monto", font=("Arial", 12)).grid(row=2, column=0, pady=(0, 10), sticky="e")
        tk.Label(frame, text="Fecha (dd-mm-aaaa)", font=("Arial", 12)).grid(row=3, column=0, pady=(0, 10), sticky="e")

        self.id_pago = tk.Entry(frame, font=("Arial", 12))
        self.id_alumno_pago = tk.Entry(frame, font=("Arial", 12))
        self.monto = tk.Entry(frame, font=("Arial", 12))
        self.fecha_pago = tk.Entry(frame, font=("Arial", 12))

        self.id_pago.grid(row=0, column=1, pady=(0, 10))
        self.id_alumno_pago.grid(row=1, column=1, pady=(0, 10))
        self.monto.grid(row=2, column=1, pady=(0, 10))
        self.fecha_pago.grid(row=3, column=1, pady=(0, 10))

        tk.Button(frame, text="Registrar Pago", command=self.registrar_pago, font=("Arial", 12)).grid(row=4, column=0, columnspan=2, pady=(20, 0))
        tk.Button(frame, text="Editar Pago", command=self.editar_pago, font=("Arial", 12)).grid(row=5, column=0, columnspan=2, pady=(10, 0))

        # Lista de pagos
        self.lista_pagos = ttk.Treeview(frame, columns=("ID Pago", "ID Alumno", "Monto", "Fecha"), show='headings')
        self.lista_pagos.heading("ID Pago", text="ID Pago")
        self.lista_pagos.heading("ID Alumno", text="ID Alumno")
        self.lista_pagos.heading("Monto", text="Monto")
        self.lista_pagos.heading("Fecha", text="Fecha")
        self.lista_pagos.grid(row=6, column=0, columnspan=2, pady=(20, 0), sticky='nsew')

        frame.rowconfigure(6, weight=1)
        frame.columnconfigure(1, weight=1)

        self.cargar_lista_pagos()

    def crear_alumno(self):
        id_alumno = self.id_alumno.get()
        nombre = self.nombre.get()
        apellido = self.apellido.get()
        correo = self.correo.get()

        if id_alumno and nombre and apellido and correo:
            self.alumnos.append({"id": id_alumno, "nombre": nombre, "apellido": apellido, "correo": correo})
            guardar_alumnos(self.alumnos)
            self.cargar_lista_alumnos()
            messagebox.showinfo("Éxito", "Alumno creado correctamente")
        else:
            messagebox.showerror("Error", "Todos los campos son obligatorios")

    def eliminar_alumno(self):
        selected_item = self.lista_alumnos.selection()
        if not selected_item:
            messagebox.showerror("Error", "Seleccione un alumno para eliminar")
            return
        respuesta = messagebox.askyesno("Confirmar", "¿Está seguro de que desea eliminar este alumno?")
        if respuesta:
            alumno_id = str(self.lista_alumnos.item(selected_item[0])['values'][0])

            print("ID del alumno seleccionado:", alumno_id)
            print("IDs de los alumnos antes de la eliminación:", [alumno['id'] for alumno in self.alumnos])
            self.alumnos = [alumno for alumno in self.alumnos if alumno['id'] != alumno_id]

            print("IDs de los alumnos después de la eliminación:", [alumno['id'] for alumno in self.alumnos])
            guardar_alumnos(self.alumnos)
            self.cargar_lista_alumnos()
            messagebox.showinfo("Éxito", "Alumno eliminado correctamente")

    def cargar_lista_alumnos(self):
        for item in self.lista_alumnos.get_children():
            self.lista_alumnos.delete(item)
        for alumno in self.alumnos:
            self.lista_alumnos.insert('', 'end', values=(alumno['id'], alumno['nombre'], alumno['apellido'], alumno['correo']))

    def editar_alumno(self):
        selected_item = self.lista_alumnos.selection()
        if not selected_item:
            messagebox.showerror("Error", "Seleccione un alumno para editar")
            return
        alumno_id = self.lista_alumnos.item(selected_item[0])['values'][0]
        for alumno in self.alumnos:
            if alumno['id'] == alumno_id:
                alumno['nombre'] = self.nombre.get()
                alumno['apellido'] = self.apellido.get()
                alumno['correo'] = self.correo.get()
                guardar_alumnos(self.alumnos)
                self.cargar_lista_alumnos()
                messagebox.showinfo("Éxito", "Alumno editado correctamente")
                return

    def registrar_pago(self):
        id_pago = self.id_pago.get()
        id_alumno = self.id_alumno_pago.get()
        monto = self.monto.get()
        fecha_pago = self.fecha_pago.get()

        try:
            datetime.strptime(fecha_pago, '%d-%m-%Y')
        except ValueError:
            messagebox.showerror("Error", "Fecha no válida. Use el formato dd-mm-aaaa")
            return

        if id_pago and id_alumno and monto and fecha_pago:
            self.pagos.append({"id_pago": id_pago, "id_alumno": id_alumno, "monto": monto, "fecha": fecha_pago})
            guardar_pagos(self.pagos)
            self.cargar_lista_pagos()
            messagebox.showinfo("Éxito", "Pago registrado correctamente")
        else:
            messagebox.showerror("Error", "Todos los campos son obligatorios")

    def cargar_lista_pagos(self):
        for item in self.lista_pagos.get_children():
            self.lista_pagos.delete(item)
        for pago in self.pagos:
            if 'id_pago' in pago and 'id_alumno' in pago and 'monto' in pago and 'fecha' in pago:
                self.lista_pagos.insert('', 'end', values=(pago['id_pago'], pago['id_alumno'], pago['monto'], pago['fecha']))
            else:
                print("Error: formato de datos incorrecto en la lista de pagos.")

    def editar_pago(self):
        selected_item = self.lista_pagos.selection()
        if not selected_item:
            messagebox.showerror("Error", "Seleccione un pago para editar")
            return
        pago_id = self.lista_pagos.item(selected_item[0])['values'][0]
        for pago in self.pagos:
            if pago['id_pago'] == pago_id:
                pago['id_alumno'] = self.id_alumno_pago.get()
                pago['monto'] = self.monto.get()
                pago['fecha'] = self.fecha_pago.get()
                guardar_pagos(self.pagos)
                self.cargar_lista_pagos()
                messagebox.showinfo("Éxito", "Pago editado correctamente")
                return

class DashboardSecretarioApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Dashboard del Secretario")
        self.root.geometry("850x500")
        self.root.resizable(False, False)

        self.alumnos = cargar_alumnos()
        self.pagos = cargar_pagos()

        self.crear_interfaz_dashboard()

    def crear_interfaz_dashboard(self):
        notebook = ttk.Notebook(self.root)

        # Pestaña Alumnos
        self.pestana_alumnos = tk.Frame(notebook)
        notebook.add(self.pestana_alumnos, text="Alumnos")
        self.crear_pestana_alumnos()

        # Pestaña Pagos
        self.pestana_pagos = tk.Frame(notebook)
        notebook.add(self.pestana_pagos, text="Pagos")
        self.crear_pestana_pagos()

        notebook.pack(expand=True, fill='both')

    def crear_pestana_alumnos(self):
        frame = tk.Frame(self.pestana_alumnos, padx=20, pady=20)
        frame.pack(expand=True, fill='both')

        # Lista de alumnos
        self.lista_alumnos = ttk.Treeview(frame, columns=("ID Alumno", "Nombre", "Apellido", "Correo"), show='headings')
        self.lista_alumnos.heading("ID Alumno", text="ID Alumno")
        self.lista_alumnos.heading("Nombre", text="Nombre")
        self.lista_alumnos.heading("Apellido", text="Apellido")
        self.lista_alumnos.heading("Correo", text="Correo")
        self.lista_alumnos.grid(row=0, column=0, columnspan=2, pady=(20, 0), sticky='nsew')

        frame.rowconfigure(0, weight=1)
        frame.columnconfigure(1, weight=1)

        self.cargar_lista_alumnos()

    def crear_pestana_pagos(self):
        frame = tk.Frame(self.pestana_pagos, padx=20, pady=20)
        frame.pack(expand=True, fill='both')

        # Formulario de registro/edición de pagos
        tk.Label(frame, text="ID Pago", font=("Arial", 12)).grid(row=0, column=0, pady=(0, 10), sticky="e")
        tk.Label(frame, text="ID Alumno", font=("Arial", 12)).grid(row=1, column=0, pady=(0, 10), sticky="e")
        tk.Label(frame, text="Monto", font=("Arial", 12)).grid(row=2, column=0, pady=(0, 10), sticky="e")
        tk.Label(frame, text="Fecha (dd-mm-aaaa)", font=("Arial", 12)).grid(row=3, column=0, pady=(0, 10), sticky="e")

        self.id_pago = tk.Entry(frame, font=("Arial", 12))
        self.id_alumno_pago = tk.Entry(frame, font=("Arial", 12))
        self.monto = tk.Entry(frame, font=("Arial", 12))
        self.fecha_pago = tk.Entry(frame, font=("Arial", 12))

        self.id_pago.grid(row=0, column=1, pady=(0, 10))
        self.id_alumno_pago.grid(row=1, column=1, pady=(0, 10))
        self.monto.grid(row=2, column=1, pady=(0, 10))
        self.fecha_pago.grid(row=3, column=1, pady=(0, 10))

        tk.Button(frame, text="Registrar Pago", command=self.registrar_pago, font=("Arial", 12)).grid(row=4, column=0,
                                                                                                      columnspan=2,
                                                                                                      pady=(20, 0))
        tk.Button(frame, text="Editar Pago", command=self.editar_pago, font=("Arial", 12)).grid(row=5, column=0,
                                                                                                columnspan=2,
                                                                                                pady=(10, 0))
        tk.Button(frame, text="Generar Reporte", command=self.generar_reporte, font=("Arial", 12)).grid(row=6, column=0,
                                                                                                        columnspan=2,
                                                                                                        pady=(10, 0))

        # Lista de pagos
        self.lista_pagos = ttk.Treeview(frame, columns=("ID Pago", "ID Alumno", "Monto", "Fecha"), show='headings')
        self.lista_pagos.heading("ID Pago", text="ID Pago")
        self.lista_pagos.heading("ID Alumno", text="ID Alumno")
        self.lista_pagos.heading("Monto", text="Monto")
        self.lista_pagos.heading("Fecha", text="Fecha")
        self.lista_pagos.grid(row=7, column=0, columnspan=2, pady=(20, 0), sticky='nsew')

        frame.rowconfigure(7, weight=1)
        frame.columnconfigure(1, weight=1)

        self.cargar_lista_pagos()

    def generar_reporte(self):
        nombre_archivo = f"reporte_pagos_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.txt"
        with open(nombre_archivo, "w") as archivo:
            archivo.write("Reporte de Pagos\n")
            archivo.write(f"Fecha: {datetime.now().strftime('%d-%m-%Y %H:%M:%S')}\n\n")
            archivo.write("ID Pago | ID Alumno | Monto | Fecha\n")
            for pago in self.pagos:
                archivo.write(f"{pago['id_pago']} | {pago['id_alumno']} | {pago['monto']} | {pago['fecha']}\n")
        messagebox.showinfo("Reporte generado", f"El reporte se ha generado como '{nombre_archivo}'")

    def cargar_lista_alumnos(self):
        for item in self.lista_alumnos.get_children():
            self.lista_alumnos.delete(item)
        for alumno in self.alumnos:
            self.lista_alumnos.insert('', 'end', values=(alumno['id'], alumno['nombre'], alumno['apellido'], alumno['correo']))

    def registrar_pago(self):
        id_pago = self.id_pago.get()
        id_alumno = self.id_alumno_pago.get()
        monto = self.monto.get()
        fecha_pago = self.fecha_pago.get()

        try:
            datetime.strptime(fecha_pago, '%d-%m-%Y')
        except ValueError:
            messagebox.showerror("Error", "Fecha no válida. Use el formato dd-mm-aaaa")
            return

        if id_pago and id_alumno and monto and fecha_pago:
            self.pagos.append({"id_pago": id_pago, "id_alumno": id_alumno, "monto": monto, "fecha": fecha_pago})
            guardar_pagos(self.pagos)
            self.cargar_lista_pagos()
            messagebox.showinfo("Éxito", "Pago registrado correctamente")
        else:
            messagebox.showerror("Error", "Todos los campos son obligatorios")

    def cargar_lista_pagos(self):
        for item in self.lista_pagos.get_children():
            self.lista_pagos.delete(item)
        for pago in self.pagos:
            if 'id_pago' in pago and 'id_alumno' in pago and 'monto' in pago and 'fecha' in pago:
                self.lista_pagos.insert('', 'end', values=(pago['id_pago'], pago['id_alumno'], pago['monto'], pago['fecha']))
            else:
                print("Error: formato de datos incorrecto en la lista de pagos.")

    def editar_pago(self):
        selected_item = self.lista_pagos.selection()
        if not selected_item:
            messagebox.showerror("Error", "Seleccione un pago para editar")
            return
        pago_id = self.lista_pagos.item(selected_item[0])['values'][0]
        for pago in self.pagos:
            if pago['id_pago'] == pago_id:
                pago['id_alumno'] = self.id_alumno_pago.get()
                pago['monto'] = self.monto.get()
                pago['fecha'] = self.fecha_pago.get()
                guardar_pagos(self.pagos)
                self.cargar_lista_pagos()
                messagebox.showinfo("Éxito", "Pago editado correctamente")
                return

if __name__ == "__main__":
    root = tk.Tk()
    app = LoginApp(root)
    root.mainloop()
