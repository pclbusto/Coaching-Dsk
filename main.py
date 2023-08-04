from Entidades import *
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from sqlalchemy import select

engine = create_engine("sqlite:///coaching.db")

session = Session(engine)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
   recurso = Recurso(nombre='Pedro', apellido='Busto')
   sesion = Sesion(fecha=date(year=2023,month=8,day=2))
   recurso.sesiones.append(sesion)
   session.add(recurso)
   recurso = Recurso(nombre='Carlos', apellido='Barzola')
   session.add(recurso)
   recurso = Recurso(nombre='Pablo', apellido='Telleria')
   session.add(recurso)

   session.commit()

   stmt = select(Recurso)
   for user in session.scalars(stmt):
      sesion = Sesion(fecha=date(year=2023, month=8, day=2))
      user.sesiones.append(sesion)
      print(user)
   session.commit()














