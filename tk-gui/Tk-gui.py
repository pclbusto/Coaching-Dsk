from tkinter import *
import tkinter as tk
from tkinter import ttk

from Entidades import *
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from sqlalchemy import insert
from helper import ModoAperturaVentana
from AdminObjetivoPrevio import Toplevel_Admin_Objetivo_Previo

class Coaching_TK_Gui(tk.Tk):
    def __init__(self):
        super().__init__()
        self.engine = create_engine("sqlite:///coaching.db", echo=False)
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

        self.boton_recurso_nuevo = Button(self.panel_nombre_recurso, text="+", command=self.abrir_ventana_admin_recurso)
        self.boton_recurso_nuevo.grid(column=0, row=0)







        # CREACION SECCION LISTA DE SESSIONES
        self.panel_separador = Frame(self.panel_izquierdo)
        self.panel_separador.grid(column=0, row=7, sticky=NSEW, columnspan=3)
        # self.separador = ttk.Separator(self.panel_separador, orient='horizontal')
        # self.separador.grid(column=0, row=0, sticky=(W, E), columnspan=3)
        self.label_lista_sesiones = Label(self.panel_separador, text="Lista Sesiones")
        self.label_lista_sesiones.grid(column=0, row=8, sticky=W)
        self.lista_sesiones = ttk.Treeview(self.panel_izquierdo, columns=['fecha'], displaycolumns=['fecha'])
        self.lista_sesiones.heading("#0", text="ID")
        self.lista_sesiones.heading(column=0, text="fecha")
        self.lista_sesiones.grid(column=0, row=9, sticky=(W,E), columnspan=3)
        self.lista_sesiones.bind("<ButtonRelease-1>", self.OnClick_lista_sesiones)

        self.boton_nueva_sesion = Button(self.panel_separador, text="+", command=self.crear_sesion)
        self.boton_borrar_sesion = Button(self.panel_separador, text="-", command=self.borrar_sesion)
        self.boton_nueva_sesion.grid(column=2, row=8, sticky=W)
        self.boton_borrar_sesion.grid(column=3, row=8, sticky=W)

        # self.boton_nueva_sesion.grid(column=1, row=10, pady=10)


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
        self.lista_objetivos_anteriores.bind("<Double-Button-1>", self.OnDoubleClick_lista_objetivos_anteriores)



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
        self.lista_objetivos_actuales.bind("<Double-Button-1>", self.OnDoubleClick_lista_objetivos_actuales)

        self.frm.pack(expand = True, fill = BOTH)
        self.inicializar_recurso()
        # self.set_recurso()
        # self.set_lista_sesiones()

    def OnDoubleClick_lista_objetivos_anteriores(self, args):
        curItem = self.lista_objetivos_anteriores.focus()
        objetivo_anterior_id = self.lista_objetivos_anteriores.item(curItem)["text"]
        print("ID objetivo_anterior_id: {}".format(objetivo_anterior_id))
        self.manager_recurso.establecer_objetivo_previo(objetivo_previo_id=objetivo_anterior_id)
        Toplevel_Admin_Objetivo_Previo(padre=root, manager=self.manager_recurso,
                                       callback=self.actualizar_list_objetivos,
                                       modo=ModoAperturaVentana.MODIFICACION)
    def OnDoubleClick_lista_objetivos_actuales(self, args):
        curItem = self.lista_objetivos_actuales.focus()
        id_objetivo = self.lista_objetivos_actuales.item(curItem)["text"]
        self.manager_recurso.establecer_objetivo(id_objetivo)
        newWindow = Toplevel_Admin_Objetivo(padre=root, manager=self.manager_recurso,
                                           sesion=self.manager_recurso.sesion_actual,
                                           callback=self.actualizar_list_objetivos,
                                            modo=ModoAperturaVentana.MODIFICACION)

    def borrar_sesion(self):
        self.manager_recurso.borrar_sesion(self.manager_recurso.sesion_actual)
        self.set_lista_sesiones()
    def crear_sesion(self):
        self.manager_recurso.crear_sesion(self.manager_recurso.recurso_actual)
        self.set_lista_sesiones()



    def inicializar_recurso(self):
        self.resultsContents = StringVar()
        self.label_nombre_recurso = Label(self.panel_nombre_recurso, text="")
        self.label_nombre_recurso['textvariable'] = self.resultsContents


        self.label_nombre_recurso.grid(column=1, row=0)
        self.boton_recurso_lookup = Button(self.panel_nombre_recurso, text="Q", command=self.abrir_lookup_recursos)

        self.boton_recurso_lookup.grid(column=2, row=0)
        self.text_datos_recurso = Text(self.panel_izquierdo, width=40, height=10, padx=10)
        self.text_datos_recurso.grid(column=0, row=2, columnspan=3, rowspan=3, sticky=NSEW)
        self.actualizar_recurso()

    def abrir_lookup_recursos(self):
        newWindow = Toplevel_Lookup_Recurso(root, self.manager_recurso, self.actualizar_recurso)
    def actualizar_recurso(self):
        """
        Esta funcion debe ordernar lo que tiene que actualizar si se cambiar el recurso. Esto es cargar la nueva
        lista de sessiones para ese recurso, seleccionar la primera sesion si es que la hay y ejecutar la
        actualizacion de cambio de sesion
        :return:
        """
        self.resultsContents.set(self.manager_recurso.recurso_actual)
        self.text_datos_recurso.delete('1.0', END)
        self.text_datos_recurso.insert(1.0, self.manager_recurso.recurso_actual.info_personal)
        self.lista_sesiones.delete(*self.lista_sesiones.get_children())
        self.set_lista_sesiones()

    def abrir_ventana_admin_recurso(self):
        newWindow = Toplevel_Admin_Recurso(padre=root, manager=self.manager_recurso, callback=self.actualizar_recurso)

    def abrir_ventana_nuevo_objetivo(self):
        newWindow = Toplevel_Admin_Objetivo(padre=root, manager=self.manager_recurso, sesion=self.manager_recurso.sesion_actual, callback=self.actualizar_list_objetivos)


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
        if curItem is not None:
            sesion_id = self.lista_sesiones.item(curItem)["text"]
            if sesion_id !='':
                self.manager_recurso.cambiar_sesion(sesion_id)
                self.manager_recurso.obtener_objetivos_anteriores()
                self.manager_recurso.obtener_objetivos()

                self.lista_objetivos_anteriores.delete(*self.lista_objetivos_anteriores.get_children())
                for objetivo_previo in self.manager_recurso.lista_objetivos_comprometidos:
                    print(objetivo_previo)
                    self.lista_objetivos_anteriores.insert('', 'end', '{}'.format(objetivo_previo.id), text='{}'.format(objetivo_previo.id), values=[self.manager_recurso.obtener_descripcion_objetivo(objetivo_previo.id), objetivo_previo.estado.name, objetivo_previo.descripcion_estado])

                self.actualizar_list_objetivos()

    def set_recurso(self):
        self.resultsContents.set(self.manager_recurso.recurso_actual)


    def set_lista_sesiones(self):
        self.manager_recurso.obtener_sessiones()
        self.lista_sesiones.delete(*self.lista_sesiones.get_children())
        for sesion in self.manager_recurso.lista_sessiones:
            self.lista_sesiones.insert('', 'end', '{}'.format(sesion.id), text='{}'.format(sesion.id), values=["{}".format(sesion.fecha)])


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

# todo crear clases para cada ventana toplevel. separar codigo
# todo mejorar la ventna creacion de recursos para que permita la modificacion. hoy solo es posible crear
# todo actualizar o recargar los objetivos previos cuando se vuelve de la ventana de edicion de objetivos previos
# todo boton o evento para pasar todo lo que no esta cerrado a objetivos nuevos para ver todo lo que se tiene que resolver.


if __name__ == "__main__":
    root = Coaching_TK_Gui()
    root.mainloop()
