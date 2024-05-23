import sqlite3

def create_database():
    conn = sqlite3.connect('colegio.db')
    cursor = conn.cursor()
    
    cursor.execute('''CREATE TABLE IF NOT EXISTS alumnos (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        nombre TEXT NOT NULL,
                        apellido TEXT NOT NULL,
                        grado TEXT NOT NULL
                    )''')
    
    cursor.execute('''CREATE TABLE IF NOT EXISTS pagos (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        alumno_id INTEGER NOT NULL,
                        monto REAL NOT NULL,
                        fecha TEXT NOT NULL,
                        FOREIGN KEY (alumno_id) REFERENCES alumnos (id)
                    )''')
    
    conn.commit()
    conn.close()

create_database()
import sqlite3

def create_database():
    conn = sqlite3.connect('colegio.db')
    cursor = conn.cursor()
    
    cursor.execute('''CREATE TABLE IF NOT EXISTS alumnos (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        nombre TEXT NOT NULL,
                        apellido TEXT NOT NULL,
                        grado TEXT NOT NULL
                    )''')
    
    cursor.execute('''CREATE TABLE IF NOT EXISTS pagos (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        alumno_id INTEGER NOT NULL,
                        monto REAL NOT NULL,
                        fecha TEXT NOT NULL,
                        FOREIGN KEY (alumno_id) REFERENCES alumnos (id)
                    )''')
    
    conn.commit()
    conn.close()

create_database()
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import sqlite3

class ColegioApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema de Pagos del Colegio")
        
        self.create_widgets()

    def create_widgets(self):
        # Crear pestañas
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(pady=10, expand=True)
        
        # Pestañas
        self.tab1 = ttk.Frame(self.notebook)
        self.tab2 = ttk.Frame(self.notebook)
        
        self.notebook.add(self.tab1, text='Alumnos')
        self.notebook.add(self.tab2, text='Pagos')
        
        #la pestaña de alumnos
        self.lbl_nombre = ttk.Label(self.tab1, text="Nombre:")
        self.lbl_nombre.grid(column=0, row=0, padx=5, pady=5)
        self.entry_nombre = ttk.Entry(self.tab1)
        self.entry_nombre.grid(column=1, row=0, padx=5, pady=5)
        
        self.lbl_apellido = ttk.Label(self.tab1, text="Apellido:")
        self.lbl_apellido.grid(column=0, row=1, padx=5, pady=5)
        self.entry_apellido = ttk.Entry(self.tab1)
        self.entry_apellido.grid(column=1, row=1, padx=5, pady=5)
        
        self.lbl_grado = ttk.Label(self.tab1, text="Grado:")
        self.lbl_grado.grid(column=0, row=2, padx=5, pady=5)
        self.entry_grado = ttk.Entry(self.tab1)
        self.entry_grado.grid(column=1, row=2, padx=5, pady=5)
        
        self.btn_agregar_alumno = ttk.Button(self.tab1, text="Agregar Alumno", command=self.agregar_alumno)
        self.btn_agregar_alumno.grid(column=0, row=3, columnspan=2, padx=5, pady=10)
        
        self.tree_alumnos = ttk.Treeview(self.tab1, columns=("ID", "Nombre", "Apellido", "Grado"), show="headings")
        self.tree_alumnos.heading("ID", text="ID")
        self.tree_alumnos.heading("Nombre", text="Nombre")
        self.tree_alumnos.heading("Apellido", text="Apellido")
        self.tree_alumnos.heading("Grado", text="Grado")
        self.tree_alumnos.grid(column=0, row=4, columnspan=2, padx=5, pady=5)
        
        self.cargar_alumnos()
        
        # pestaña de pagos
        self.lbl_alumno_id = ttk.Label(self.tab2, text="ID Alumno:")
        self.lbl_alumno_id.grid(column=0, row=0, padx=5, pady=5)
        self.entry_alumno_id = ttk.Entry(self.tab2)
        self.entry_alumno_id.grid(column=1, row=0, padx=5, pady=5)
        
        self.lbl_monto = ttk.Label(self.tab2, text="Monto:")
        self.lbl_monto.grid(column=0, row=1, padx=5, pady=5)
        self.entry_monto = ttk.Entry(self.tab2)
        self.entry_monto.grid(column=1, row=1, padx=5, pady=5)
        
        self.lbl_fecha = ttk.Label(self.tab2, text="Fecha:")
        self.lbl_fecha.grid(column=0, row=2, padx=5, pady=5)
        self.entry_fecha = ttk.Entry(self.tab2)
        self.entry_fecha.grid(column=1, row=2, padx=5, pady=5)
        
        self.btn_registrar_pago = ttk.Button(self.tab2, text="Registrar Pago", command=self.registrar_pago)
        self.btn_registrar_pago.grid(column=0, row=3, columnspan=2, padx=5, pady=10)
        
        self.tree_pagos = ttk.Treeview(self.tab2, columns=("ID", "Alumno ID", "Monto", "Fecha"), show="headings")
        self.tree_pagos.heading("ID", text="ID")
        self.tree_pagos.heading("Alumno ID", text="Alumno ID")
        self.tree_pagos.heading("Monto", text="Monto")
        self.tree_pagos.heading("Fecha", text="Fecha")
        self.tree_pagos.grid(column=0, row=4, columnspan=2, padx=5, pady=5)
        
        self.cargar_pagos()

    def agregar_alumno(self):
        nombre = self.entry_nombre.get()
        apellido = self.entry_apellido.get()
        grado = self.entry_grado.get()
        
        if nombre and apellido and grado:
            conn = sqlite3.connect('colegio.db')
            cursor = conn.cursor()
            cursor.execute("INSERT INTO alumnos (nombre, apellido, grado) VALUES (?, ?, ?)", (nombre, apellido, grado))
            conn.commit()
            conn.close()
            messagebox.showinfo("Éxito", "Alumno agregado correctamente")
            self.cargar_alumnos()
        else:
            messagebox.showerror("Error", "Todos los campos son obligatorios")

    def cargar_alumnos(self):
        for row in self.tree_alumnos.get_children():
            self.tree_alumnos.delete(row)
        
        conn = sqlite3.connect('colegio.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM alumnos")
        rows = cursor.fetchall()
        
        for row in rows:
            self.tree_alumnos.insert("", tk.END, values=row)
        
        conn.close()

    def registrar_pago(self):
        alumno_id = self.entry_alumno_id.get()
        monto = self.entry_monto.get()
        fecha = self.entry_fecha.get()
        
        if alumno_id and monto and fecha:
            conn = sqlite3.connect('colegio.db')
            cursor = conn.cursor()
            cursor.execute("INSERT INTO pagos (alumno_id, monto, fecha) VALUES (?, ?, ?)", (alumno_id, monto, fecha))
            conn.commit()
            conn.close()
            messagebox.showinfo("Éxito", "Pago registrado correctamente")
            self.cargar_pagos()
        else:
            messagebox.showerror("Error", "Todos los campos son obligatorios")
        
    def cargar_pagos(self):
        for row in self.tree_pagos.get_children():
            self.tree_pagos.delete(row)
        
        conn = sqlite3.connect('colegio.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM pagos")
        rows = cursor.fetchall()
        
        for row in rows:
            self.tree_pagos.insert("", tk.END, values=row)
        
        conn.close()

if __name__ == "__main__":
    root = tk.Tk()
    app = ColegioApp(root)
    root.mainloop()
