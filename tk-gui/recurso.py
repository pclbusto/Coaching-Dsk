from tkinter import *
from tkinter import ttk

from Entidades import *
from sqlalchemy import insert
from helper import ModoAperturaVentana

class Toplevel_Lookup_Recurso(Toplevel):
    def __init__(self, padre, manager, callback):
        super().__init__(padre)
        self.manager = manager
        self.callback = callback
        self.title("Lookup Recurso")
        self.geometry("440x260")
        self.frm = ttk.Frame(self)
        self.lista_recursos = ttk.Treeview(self.frm, columns=['nombre', 'apellido'],
                                           displaycolumns=['nombre', 'apellido'])

        self.lista_recursos.grid(column=0, row=0, sticky=(E, W, N, S))
        self.lista_recursos.column('#0', width=30, stretch=NO)
        self.lista_recursos.heading('#0', text='Id')
        self.lista_recursos.heading('nombre', text='Nombre')
        self.lista_recursos.heading('apellido', text='Apellido')
        self.lista_recursos.bind("<Double-Button-1>", self.lista_recursos_double_click)
        self.manager.obtener_recursos()
        for recurso in self.manager.recursos:
            # print(type(recurso))
            self.lista_recursos.insert('', 'end', '{}'.format(recurso.id), text='{}'.format(recurso.id),
                                       values=[recurso.nombre, recurso.apellido])

        self.boton_seleccionar = Button(self.frm, text="seleccionar", command=self.seleccionar_cerrar)
        self.boton_seleccionar.grid(column=0, row=1, sticky=E)
        self.frm.grid(column=0, row=0)
    def lista_recursos_double_click(self, args):
        self.cerrar()
    def seleccionar_cerrar(self):
        self.cerrar()
    def cerrar(self):
        curItem = self.lista_recursos.focus()
        recurso_id = self.lista_recursos.item(curItem)["text"]
        self.manager.establecer_recurso(recurso_id)
        self.callback()
        self.destroy()

class Toplevel_Admin_Recurso(Toplevel):
    def __init__(self, padre, manager:ManagerRecurso, callback, modo=ModoAperturaVentana.CREACION):
        super().__init__(padre)
        self.manager = manager
        self.callback = callback
        self.title("Recurso")
        self.geometry("600x360")
        self.frm = ttk.Frame(self)
        self.label_nombre = Label(self.frm, text='Nombre')
        self.label_nombre.grid(column=0, row=0)
        self.entry_nombre_var = StringVar()
        self.entry_nombre = Entry(self.frm, textvariable=self.entry_nombre_var)
        self.entry_nombre.grid(column=1, row=0)
        self.label_apellido = Label(self.frm, text='Apellido')
        self.label_apellido.grid(column=0, row=1)
        self.entry_apellido_var = StringVar()
        self.entry_apellido = Entry(self.frm, textvariable=self.entry_apellido_var)
        self.entry_apellido.grid(column=1, row=1)
        self.descripcion = Text(self.frm, width=40, height=10, pady=10)
        self.descripcion.grid(column=3, row=0, sticky=(E, W, N, S), rowspan=3, padx=5, pady=5)
        self.boton_guardar = Button(self.frm, text="Guardar", command=self.guardar_cerrar)
        self.boton_guardar.grid(column=3, row=7, sticky=E, padx=5)
        self.frm.pack()

    def guardar_cerrar(self):
        self.manager.sesion_sql_alchemy.execute(insert(Recurso).values(nombre=self.entry_nombre_var.get(),
                                                            apellido=self.entry_apellido_var.get(),
                                                            info_personal=self.descripcion.get('1.0', 'end')))
        self.manager.sesion_sql_alchemy.commit()
        self.callback()
        self.destroy()