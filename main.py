from Entidades import *
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from sqlalchemy import select

engine = create_engine("sqlite:///coaching.db")

session = Session(engine)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
   recurso = Recurso(nombre='Pedro', apellido='Busto', info_personal= 'Originally thought to be chosen by chance, it was later revealed that Ganthet chose Kyle Rayner because he had the ability to harness the powers of the emotional spectrum. Once the Torchbearer of the Green Lantern Corps, Kyle graduated to the role Ganthet had intended for him: the White Lantern. After the White Ring is separated into seven rings, Kyle returns to being a Green Lantern Corpsman.')
   sesion = Sesion(fecha=date(year=2023,month=8,day=2))
   recurso.sesiones.append(sesion)
   session.add(recurso)
   recurso = Recurso(nombre='Carlos', apellido='Barzola', info_personal='Formerly an architect, social activist, and U.S. Marine sniper, John Stewart was chosen by the Guardians of the Universe to join the Green Lantern Corps, an intergalactic peacekeeping organization dedicated to protecting life throughout the universe. Stewart has proven himself time and again to be an exceptional champion in countless missions that have taken him across the cosmos. His distinguished service in the Corps has resulted in a place among the Oan Honor Guard and the position of Corps Leader.')
   session.add(recurso)
   recurso = Recurso(nombre='Pablo', apellido='Telleria', info_personal='With the ability to overcome great fear and harness the power of will, test-pilot Hal Jordan was chosen to be the Green Lantern of Sector 2814 inheriting the ring of the dying alien Green Lantern, Abin Sur. He later on went to creating his own power ring from his own will power. Through sheer will power and determination, Hal has established an impressive record of heroism across the galaxy with the help of his fellow Green Lanterns as well as his peers in the Justice League.')
   session.add(recurso)

   session.commit()

   stmt = select(Recurso)
   for user in session.scalars(stmt):
      sesion = Sesion(fecha=date(year=2023, month=8, day=2))
      user.sesiones.append(sesion)
      print(user)
   session.commit()














