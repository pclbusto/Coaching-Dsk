from tkinter import *
import tkinter as tk
from tkinter import ttk

from Entidades import *
from sqlalchemy.orm import Session
from sqlalchemy import create_engine



class Coaching_TK_Gui(tk.Tk):
    def __init__(self):
        super().__init__()
        self.engine = create_engine("sqlite:///coaching.db")
        self.session = Session(self.engine)
        self.manager_recurso = ManagerRecurso(sesion_sql_alchemy=self.session)


        self.frm = Frame(self,  background='red' )
        self.frm.grid(column=0, row=0, sticky=(N, W, E, S))

        self.panel_izquierdo = ttk.Frame(self.frm, padding=10)
        self.panel_izquierdo.grid(column=0, row=0, sticky=(N, W, S))
        self.panel_separador_vertical = Frame(self.frm)
        self.panel_separador_vertical.grid(column=1, row=1, sticky=(N, S), rowspan=2)
        # self.separador.grid(column=1, row=0, sticky=(N, S, E), rowspan=4)
        self.panel_derecho = ttk.Frame(self.frm, padding=10)
        self.panel_derecho.grid(column=2, row=0, sticky=(N, E, S))

        self.frm.columnconfigure(0, weight=3)
        self.frm.columnconfigure(1, weight=1)
        self.frm.columnconfigure(0, weight=6)
        self.panel_nombre_recurso = ttk.Frame(self.panel_izquierdo, padding=10)
        self.panel_nombre_recurso.grid(column=0, row=0, columnspan=3)

        self.boton_recurso_nuevo = Button(self.panel_nombre_recurso, text="+")
        self.boton_recurso_nuevo.grid(column=0, row=0)

        self.resultsContents = StringVar()

        self.label_nombre_recurso = Label(self.panel_nombre_recurso, text="Juan Perez")
        self.label_nombre_recurso['textvariable'] = self.resultsContents

        self.label_nombre_recurso.grid(column=1, row=0)
        self.boton_recurso_lookup = Button(self.panel_nombre_recurso, text="Q")
        self.boton_recurso_lookup.grid(column=2, row=0)
        self.text_datos_recurso = Text(self.panel_izquierdo,  width=40, height=10, padx=10)
        self.text_datos_recurso.grid(column=0, row=2, columnspan=3, rowspan=3, sticky=NSEW)
        self.text_datos_recurso.insert(1.0, "Resumen de las cosas relevantes que ha estado haciendo. Hobies y cosas de indole personal")


        # CREACION SECCION LISTA DE SESSIONES
        self.panel_separador = Frame(self.panel_izquierdo)
        self.panel_separador.grid(column=0, row=7, sticky=NSEW, columnspan=3)
        # self.separador = ttk.Separator(self.panel_separador, orient='horizontal')
        # self.separador.grid(column=0, row=0, sticky=(W, E), columnspan=3)
        self.label_lista_sesiones = Label(self.panel_izquierdo, text="Lista Sesiones")
        self.label_lista_sesiones.grid(column=0, row=8, sticky=W)
        self.lista_sesiones = ttk.Treeview(self.panel_izquierdo, columns=['fecha'], displaycolumns=['fecha'])
        self.lista_sesiones.heading("#0", text="ID")
        self.lista_sesiones.heading(column=0, text="fecha")
        self.lista_sesiones.grid(column=0, row=9, sticky=(W,E), columnspan=3)
        self.boton_nueva_sesion = Button(self.panel_izquierdo, text="nueva sesión")
        self.boton_nueva_sesion.grid(column=1, row=10, pady=10)

        self.set_recurso()
        self.set_lista_sesiones()

        #panel objetivos sesion pasada
        self.lista_objetivos_anteriores = ttk.Treeview(self.panel_derecho, columns=['id','objetivos pactados', 'estado', 'justificacion estado'], displaycolumns=['id','objetivos pactados', 'estado', 'justificacion estado'])
        self.lista_objetivos_anteriores.grid(column=0, row=0)
        #panel separador
        self.panel_separador_objetivos = ttk.Frame(self.panel_derecho, padding=15, height=10)
        self.panel_separador_objetivos.grid(column=0, row=1)
        # panel objetivos sesion actual
        self.lista_objetivos_anteriores = ttk.Treeview(self.panel_derecho,
                                                       columns=['id', 'objetivos pactados'],
                                                       displaycolumns=['id', 'objetivos pactados'])
        self.lista_objetivos_anteriores.grid(column=0, row=2, sticky=(W,E))

        self.frm.pack(expand = True, fill = BOTH)
        print("Hola")

    def set_recurso(self):
        self.resultsContents.set(self.manager_recurso.recurso_actual)


    def set_lista_sesiones(self):
        self.manager_recurso.obtener_sessiones()
        for sesion in self.manager_recurso.lista_sessiones:
            self.lista_sesiones.insert('', 'end', '{}'.format(sesion.id), text='{}'.format(sesion.id), values=["{}".format(sesion.fecha)])

if __name__ == "__main__":
    root = Coaching_TK_Gui()
    root.mainloop()
