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

class ObjetivosComprometidos(Base):
    __tablename__ = "objetivo"
    id: Mapped[int] = mapped_column(primary_key=True)
    descripcion: Mapped[str] = mapped_column(String)
    session_id = mapped_column(ForeignKey("recurso.id"))


class ManagerRecurso():
    def __init__(self, sesion_sql_alchemy):
        self.sesion_sql_alchemy =sesion_sql_alchemy
        self.init_recurso()

        self.lista_sessiones = []
        self.lista_objetivos_actuales = []
        self.lista_objetivos_comprometidos = []

    def init_recurso(self):
        self.recurso_actual = self.sesion_sql_alchemy.execute(select(Recurso).order_by(Recurso.id)).first()[0]
        print(self.recurso_actual)

    def obtener_sessiones(self):
        if self.recurso_actual is not None:
            print("ID recurso para recuperar las sesiones {}".format(self.recurso_actual.id))
            stmt = select(Sesion).where(Sesion.recurso_id == self.recurso_actual.id)
            for sesion in self.sesion_sql_alchemy.scalars(stmt):
                self.lista_sessiones.append(sesion)
            print(self.lista_sessiones)





