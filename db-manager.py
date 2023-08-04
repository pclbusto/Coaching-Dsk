from sqlalchemy import create_engine
from Entidades import *

engine = create_engine("sqlite:///coaching.db")
Base.metadata.drop_all(engine)
Base.metadata.create_all(engine)
