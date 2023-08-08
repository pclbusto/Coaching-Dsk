# from typing import List
# from typing import Optional
from sqlalchemy import ForeignKey
from sqlalchemy import String, Date, Enum
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from datetime import date
from typing import List
from sqlalchemy.orm import relationship
from enum import Enum as PyEnum
from sqlalchemy import select

from sqlalchemy import delete
from sqlalchemy import insert
from sqlalchemy import update
from sqlalchemy import func


class StatusEnum(PyEnum):
    ACTIVO = 'Activo'
    PENDIENTE = 'Pendiente'
    CERRADO = 'Cerrado'


class Base(DeclarativeBase):
    pass

class Recurso(Base):
    __tablename__ = "recurso"
    id: Mapped[int] = mapped_column(primary_key=True)
    nombre: Mapped[str] = mapped_column(String(30))
    apellido : Mapped[str] = mapped_column(String(30))
    sesiones : Mapped[List['Sesion']]= relationship('Sesion')
    info_personal: Mapped[str] = mapped_column(String)

    def __str__(self):
        return "{}-{}-{}".format(self.id,self.nombre, self.apellido)

class Sesion(Base):
    __tablename__ = "sesion"
    id: Mapped[int] = mapped_column(primary_key=True)
    fecha: Mapped[date] = mapped_column(Date)
    recurso_id = mapped_column(ForeignKey("recurso.id"))
    recurso: Mapped['Recurso'] = relationship("Recurso")

class ObjetivosComprometidosPreviamente(Base):
    __tablename__ = "objetivos_previos"
    id: Mapped[int] = mapped_column(primary_key=True)
    objetivo_original_id = mapped_column(ForeignKey("objetivo.id"))
    session_id = mapped_column(ForeignKey("recurso.id"))
    estado: Mapped[StatusEnum] = mapped_column(Enum(StatusEnum))
    descripcion_estado: Mapped[str] = mapped_column(String)

class ObjetivosComprometidos(Base):
    __tablename__ = "objetivo"
    id: Mapped[int] = mapped_column(primary_key=True)
    descripcion: Mapped[str] = mapped_column(String)
    session_id = mapped_column(ForeignKey("recurso.id"))


class ManagerRecurso():


    def __init__(self, sesion_sql_alchemy):

        self.sesion_sql_alchemy =sesion_sql_alchemy
        self.init_recurso()
        self.sesion_actual = None
        self.lista_sessiones = []
        self.lista_objetivos_actuales = []
        self.lista_objetivos_comprometidos = []
        self.objetivo_previo = None

    def establecer_objetivo_previo(self,objetivo_previo_id):
        self.objetivo_previo = self.sesion_sql_alchemy.execute(select(ObjetivosComprometidosPreviamente).where(ObjetivosComprometidosPreviamente.id==objetivo_previo_id)).scalars().first()
    def obtener_descripcion_objetivo(self, objetivo_id:int)->str:
        return self.sesion_sql_alchemy.execute(select(ObjetivosComprometidos).where(ObjetivosComprometidos.id==objetivo_id)).scalars().first().descripcion
    def establecer_objetivo(self, objetivo_id):
        """
        establece cual es el objetivo actual en el cual se va a trabajar. La idea es que esto se use en conjunto
        con una lista donde el elemento seleccionado se corresponda con el objetivo actual.
        :param objetivo_id: id del objetivo sobre el cual vamos a trabajar
        :return:
        """
        self.objetivo_actual = self.sesion_sql_alchemy.execute(
            select(ObjetivosComprometidos).where(ObjetivosComprometidos.id == objetivo_id)).scalars().first()

    def actualizar_objetivo(self, descripcion):
        '''
        cambia la descripcion de un objetivo. el objetivo al cual se le cambia la descripcion es el que esta en
        objetivo actual.
        :param descripcion: nueva descripcion para el objetivo
        :return:
        '''
        self.sesion_sql_alchemy.execute(update(ObjetivosComprometidos).where(ObjetivosComprometidos.id == self.objetivo_actual.id).values(descripcion= descripcion))
        self.sesion_sql_alchemy.commit()
    def borrar_objetivo_actual(self, id):
        self.sesion_sql_alchemy.execute(delete(ObjetivosComprometidos).where(ObjetivosComprometidos.id==id))
        self.sesion_sql_alchemy.commit()

    def establecer_recurso(self, recurso_id):
        self.recurso_actual = self.sesion_sql_alchemy.execute(select(Recurso).where(Recurso.id == recurso_id)).scalars().first()
        self.obtener_sessiones()


    def init_recurso(self):
        self.recurso_actual = self.sesion_sql_alchemy.execute(select(Recurso).order_by(Recurso.id)).first()[0]
        print(self.recurso_actual)
    def obtener_sessiones(self):
        if self.recurso_actual is not None:
            self.lista_sessiones.clear()
            print("ID recurso para recuperar las sesiones {}".format(self.recurso_actual.id))
            stmt = select(Sesion).where(Sesion.recurso_id == self.recurso_actual.id)
            for sesion in self.sesion_sql_alchemy.scalars(stmt):
                self.lista_sessiones.append(sesion)
    def obtener_recursos(self, orden=None):
        lista=None

        if orden is not None:
            self.recursos = self.sesion_sql_alchemy.execute.scalar(select(Recurso).order_by(orden)).scalars()
        else:
            self.recursos = self.sesion_sql_alchemy.execute(select(Recurso).order_by(Recurso.id)).scalars()

    def cambiar_sesion(self, sesion_id):
        resultado = self.sesion_sql_alchemy.execute(select(Sesion).where(Sesion.id==sesion_id)).first()
        if resultado is not None:
            self.sesion_actual = self.sesion_sql_alchemy.execute(select(Sesion).where(Sesion.id==sesion_id)).first()[0]

    def obtener_objetivos_anteriores(self):
        self.lista_objetivos_comprometidos.clear()
        stmt = select(ObjetivosComprometidosPreviamente).where(ObjetivosComprometidosPreviamente.session_id == self.sesion_actual.id)
        for objetivo_previo in self.sesion_sql_alchemy.scalars(stmt):
            self.lista_objetivos_comprometidos.append(objetivo_previo)

    def obtener_objetivos(self):
        self.lista_objetivos_actuales.clear()
        stmt = select(ObjetivosComprometidos).where(
            ObjetivosComprometidos.session_id == self.sesion_actual.id)
        for objetivo in self.sesion_sql_alchemy.scalars(stmt):
            self.lista_objetivos_actuales.append(objetivo)

    def crear_sesion(self, recurso:Recurso):
        self.sesion_sql_alchemy.execute(insert(Sesion).values(fecha=date.today(), recurso_id=recurso.id))
        self.sesion_sql_alchemy.commit()
        ultima_sesion = self.sesion_sql_alchemy.execute(select(Sesion).where(Sesion.recurso_id==recurso.id).order_by(Sesion.id.desc())).first()[0]
        sesion_previa = self.sesion_sql_alchemy.execute(select(Sesion).where(Sesion.id<ultima_sesion.id).order_by(Sesion.id.desc())).first()[0]

        lista_objetivo_previos = self.sesion_sql_alchemy.execute(select(ObjetivosComprometidos).where(ObjetivosComprometidos.session_id==sesion_previa.id)).scalars()
        for objetivo in lista_objetivo_previos:
            self.sesion_sql_alchemy.execute(insert(ObjetivosComprometidosPreviamente).values(objetivo_original_id = objetivo.id,
                                                                                             session_id = ultima_sesion.id,
                                                                                             estado = StatusEnum.ACTIVO,
                                                                                             descripcion_estado=''))
        self.sesion_sql_alchemy.commit()


    def borrar_sesion(self, sesion:Sesion):
        self.sesion_sql_alchemy.execute(delete(Sesion).where(Sesion.id == sesion.id))
        self.sesion_sql_alchemy.commit()






