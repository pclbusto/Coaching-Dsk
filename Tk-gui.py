from tkinter import *
import tkinter as tk
from tkinter import ttk

from Entidades import *
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from sqlalchemy import insert


class Coaching_TK_Gui(tk.Tk):
    def __init__(self):
        super().__init__()
        self.engine = create_engine("sqlite:///coaching.db", echo=True)
        self.session = Session(self.engine)
        self.manager_recurso = ManagerRecurso(sesion_sql_alchemy=self.session)


        self.frm = Frame(self )
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
        self.lista_sesiones.bind("<ButtonRelease-1>", self.OnClick_lista_sesiones)

        self.boton_nueva_sesion = Button(self.panel_izquierdo, text="nueva sesión")
        self.boton_nueva_sesion.grid(column=1, row=10, pady=10)

        self.set_recurso()
        self.set_lista_sesiones()

        #panel objetivos sesion pasada
        self.label_objetivos_sesion_pasada = Label(self.panel_derecho, text="Objetivos sesión pasada")
        self.label_objetivos_sesion_pasada.grid(column=0, row=0, sticky=W)
        self.lista_objetivos_anteriores = ttk.Treeview(self.panel_derecho, columns=['objetivos pactados', 'estado', 'justificacion estado'], displaycolumns=['objetivos pactados', 'estado', 'justificacion estado'])
        self.lista_objetivos_anteriores.heading("#0", text='id')
        self.lista_objetivos_anteriores.column('#0', width=30, stretch=NO)
        self.lista_objetivos_anteriores.heading(column=0, text='objetivos pactados')
        self.lista_objetivos_anteriores.heading(column=1, text='estado')
        self.lista_objetivos_anteriores.heading(column=2, text='justificacion estado')
        self.lista_objetivos_anteriores.grid(column=0, row=1)

        #panel separador
        self.panel_separador_objetivos = ttk.Frame(self.panel_derecho, padding=15, height=10)
        self.panel_separador_objetivos.grid(column=0, row=2, sticky=(W,E))
        self.label_objetivos_sesion = Label(self.panel_separador_objetivos, text="Objetivos sesión")
        self.label_objetivos_sesion.grid(column=0, row=0, sticky=W)

        # panel objetivos sesion actual
        self.boton_nuevo_objetivo = Button(self.panel_separador_objetivos, text="+", height=1, width=1, command=self.abrir_ventana_nuevo_objetivo)
        self.boton_nuevo_objetivo.grid(column=4, row=0, sticky=E)
        self.boton_eliminar_objetivo = Button(self.panel_separador_objetivos, text="-", height=1, width=1, command=self.borrar_objetivo)
        self.boton_eliminar_objetivo.grid(column=5, row=0, sticky=E)

        self.lista_objetivos_actuales = ttk.Treeview(self.panel_derecho,
                                                       columns=['objetivos pactados'],
                                                       displaycolumns=['objetivos pactados'])
        self.lista_objetivos_actuales.heading('#0', text="id")
        self.lista_objetivos_actuales.column('#0', width=30,  stretch=NO)
        self.lista_objetivos_actuales.heading(column=0, text="objetivos pactados")
        self.lista_objetivos_actuales.grid(column=0, row=4, sticky=(W,E))

        self.frm.pack(expand = True, fill = BOTH)
        print("Hola")

    def abrir_ventana_nuevo_objetivo(self):
        newWindow = Toplevel_NuevoObjetivo(root, self.session, self.manager_recurso.sesion_actual, self.actualizar_list_objetivos)


    def borrar_objetivo(self):
        curItem = self.lista_objetivos_actuales.focus()
        id_objetivo = self.lista_objetivos_actuales.item(curItem)["text"]
        self.manager_recurso.borrar_objetivo_actual(id_objetivo)
        self.actualizar_list_objetivos()
    def actualizar_list_objetivos(self):
        self.lista_objetivos_actuales.delete(*self.lista_objetivos_actuales.get_children())
        self.manager_recurso.obtener_objetivos()
        for objetivo in self.manager_recurso.lista_objetivos_actuales:
            print(objetivo)
            self.lista_objetivos_actuales.insert('', 'end', '{}'.format(objetivo.id), text='{}'.format(objetivo.id),
                                                 values=["{}".format(objetivo.descripcion)])

    def OnClick_lista_sesiones(self, args):
        curItem = self.lista_sesiones.focus()
        sesion_id = self.lista_sesiones.item(curItem)["text"]
        self.manager_recurso.cambiar_sesion(sesion_id)
        self.manager_recurso.obtener_objetivos_anteriores()
        self.manager_recurso.obtener_objetivos()

        self.lista_objetivos_anteriores.delete(*self.lista_objetivos_anteriores.get_children())
        for objetivo_previo in self.manager_recurso.lista_objetivos_comprometidos:
            print(objetivo_previo)
            self.lista_objetivos_anteriores.insert('', 'end', '{}'.format(objetivo_previo.id), text='{}'.format(objetivo_previo.id), values=["{}".format(sesion.fecha)])

        self.actualizar_list_objetivos()

    def set_recurso(self):
        self.resultsContents.set(self.manager_recurso.recurso_actual)


    def set_lista_sesiones(self):
        self.manager_recurso.obtener_sessiones()
        for sesion in self.manager_recurso.lista_sessiones:
            self.lista_sesiones.insert('', 'end', '{}'.format(sesion.id), text='{}'.format(sesion.id), values=["{}".format(sesion.fecha)])

class Toplevel_NuevoObjetivo(Toplevel):
    def __init__(self, padre, session_alchemy, session , callback):
        super().__init__(padre)
        self.session_alchemy = session_alchemy
        self.callback = callback
        self.session = session
        self.title("Nuevo Objetivo")
        self.geometry("300x220")
        self.frm = ttk.Frame(self)
        self.descripcion = Text(self.frm,  width=40, height=10, pady=10)
        self.descripcion.grid(column=0, row=0, sticky=(E,W,N,S))
        self.boton_guardar = Button(self.frm, text="Guardar", command=self.guardar_cerrar)
        self.boton_guardar.grid(column=0, row=1)
        self.frm.grid(column=0, row=0)
    def guardar_cerrar(self):
        self.session_alchemy.execute(insert(ObjetivosComprometidos).values(descripcion= self.descripcion.get('1.0', 'end'), session_id=self.session.id))
        self.session_alchemy.commit()
        self.callback()
        self.destroy()

if __name__ == "__main__":
    root = Coaching_TK_Gui()
    root.mainloop()
