from tkinter import *
import tkinter as tk
from tkinter import ttk
from  helper import ModoAperturaVentana
from sqlalchemy import insert, update
from Entidades import *
class Toplevel_Admin_Objetivo(Toplevel):
    def __init__(self, padre, manager, sesion , callback, modo=ModoAperturaVentana.CREACION):
        super().__init__(padre)
        self.manager = manager
        self.callback = callback
        self.sesion = sesion
        self.title("Admin Objetivo")
        self.geometry("335x220")
        self.frm = ttk.Frame(self)
        self.modo = modo
        self.descripcion = Text(self.frm, width=40, height=10, pady=10)
        self.descripcion.grid(column=0, row=1, sticky=(E, W, N, S), padx=5, pady=5)
        if self.modo == ModoAperturaVentana.MODIFICACION:
            self.label_id = Label(self.frm, text="ID:{}".format(self.manager.objetivo_actual.id))
            self.descripcion.insert(1.0, self.manager.objetivo_actual.descripcion)
        boton_cerrar_text = ''
        if self.modo == ModoAperturaVentana.MODIFICACION:
            boton_cerrar_text = 'Actualizar'
        elif self.modo == ModoAperturaVentana.CREACION:
            boton_cerrar_text = 'Guardar'
        self.boton_guardar = Button(self.frm, text=boton_cerrar_text, command=self.guardar_cerrar)
        self.boton_guardar.grid(column=0, row=2)
        self.frm.grid(column=0, row=0)

    def guardar_cerrar(self):
        if self.modo == ModoAperturaVentana.CREACION:
            self.manager.sesion_sql_alchemy.execute(
                insert(ObjetivosComprometidos).values(descripcion=self.descripcion.get('1.0', 'end'),
                                                      session_id=self.sesion.id))
        elif self.modo == ModoAperturaVentana.MODIFICACION:
            self.manager.sesion_sql_alchemy.execute(
                update(ObjetivosComprometidos).where(ObjetivosComprometidos.id == self.manager.objetivo_actual.id).values(descripcion=self.descripcion.get('1.0', 'end')))
        self.manager.sesion_sql_alchemy.commit()
        self.callback()
        self.destroy()

