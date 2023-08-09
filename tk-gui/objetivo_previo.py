from tkinter import *
import tkinter as tk
from tkinter import ttk

from Entidades import *
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from sqlalchemy import insert
from helper import ModoAperturaVentana
from Entidades import StatusEnum

class Toplevel_Admin_Objetivo_Previo(Toplevel):
    def __init__(self, padre, manager:ManagerRecurso, callback, modo=ModoAperturaVentana.CREACION):
        super().__init__(padre)
        self.manager = manager
        self.callback = callback
        self.title("Objetivo Previo")
        self.geometry("350x460")
        self.frm = ttk.Frame(self)
        self.label_descripcion_objetivo = Label(self.frm, text='Descripción')
        self.label_descripcion_objetivo.grid(column=0, row=0)
        self.text_descripcion_objetivo = Text(self.frm, width=40, height=10, pady=10)
        self.text_descripcion_objetivo.grid(column=0, row=1, sticky=(E, W, N, S), columnspan=2, padx=5, pady=5)
        print(self.manager.objetivo_previo.id, self.manager.objetivo_previo.objetivo_original_id, self.manager.objetivo_previo.estado, self.manager.objetivo_previo.descripcion_estado)
        self.text_descripcion_objetivo.insert('1.0',self.manager.obtener_descripcion_objetivo(self.manager.objetivo_previo.objetivo_original_id))
        self.label_estado = Label(self.frm, text='Estado')
        self.label_estado.grid(column=0, row=2)
        opciones = []
        for estado in StatusEnum:
            opciones.append(estado.name)
        self.listbox_estado_var = StringVar()
        self.listbox_estado = ttk.Combobox(self.frm,textvariable=self.listbox_estado_var, values=opciones)
        self.listbox_estado_var.set(self.manager.objetivo_previo.estado.name)
        self.listbox_estado.grid(column=1, row=2)
        self.text_justificacion_estado = Text(self.frm, width=40, height=10, pady=10)
        self.text_justificacion_estado.grid(column=0, row=3, sticky=(E, W, N, S), columnspan=2, padx=5, pady=5)
        self.text_justificacion_estado.insert('1.0', self.manager.objetivo_previo.descripcion_estado)
        self.boton_guardar = Button(self.frm, text="Guardar", command=self.guardar_cerrar)
        self.boton_guardar.grid(column=1, row=7, sticky=E, padx=5)
        self.frm.pack()


    def guardar_cerrar(self):
        self.manager.sesion_sql_alchemy.execute(update(ObjetivosComprometidosPreviamente).where(
            ObjetivosComprometidosPreviamente.id == self.manager.objetivo_previo.id).values(
            estado=self.listbox_estado_var.get(),
            descripcion_estado=self.text_justificacion_estado.get('1.0', 'end')))
        self.manager.sesion_sql_alchemy.commit()
        self.callback()
        self.destroy()
    def establecer_modo(self, modo:ModoAperturaVentana):
        pass
    #     todo: armar logica para que la ventana tome el modo correspondiente.
