import sqlalchemy,databases
from fastapi import FastAPI
from pydantic import BaseModel,Field
from typing import List
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy import Column, String , Float 

## postgres database
DATABASE_URL = "postgresql://postgres:123@127.0.0.1:5432/db"
database = databases.Database(DATABASE_URL)
metadata = sqlalchemy.MetaData()
Base = declarative_base()


engine = sqlalchemy.create_engine(
    DATABASE_URL
)
metadata.create_all(engine)

# Models
class Fruits(Base):
    __tablename__ = "fruits"

    name = Column(String, primary_key=True)
    alias = Column(String)
    varities = Column(String)

    #prod_items = relationship("Productions",back_populates="var")

class Productions(BaseModel):
    __tablename__ = "Production"
    
    name = Column(String, ForeignKey('Fruits.name'))
    country = Column(String)
    tons_produced : Column(String)

    var = relationship("Fruits",back_populates="Production")    

Fruits.production = relationship("Productions", order_by = Productions.name, back_populates = "fruits")

Base.metadata.create_all(engine)
   

app = FastAPI()

@app.on_event("startup")
async def startup():
    await database.connect()

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


@app.get("/fruits",response_model=List[fruitlist])
async def find_fruits(search:str=""):
    query = 'SELECT name,alias,varities FROM  FRUITS '\
    "WHERE name like '%"+search+"%'"
    print(query)
    var= await database.fetch_all(query)
    return var 

@app.get("/production",response_model=List[production_fruit])
async def find_production_fruit(search:str=""):
   
    query = 'SELECT FRUITS.name,FRUITS.alias,varities,country,tons_produced FROM  FRUITS JOIN PRODUCTION ON FRUITS.name=PRODUCTION.name '\
    "WHERE FRUITS.name like '%"+search+"%'"
    #print(query)
    var= await database.fetch_all(query)
    return var     

@app.post("/fruits",response_model=fruitlist)
async def register_fruit(user: fruitEntry):
    
    query = fruits.insert().values(
        name = user.name,
        alias = user.alias,
        varities = user.varities
        
    )

    await database.execute(query)
    return {
        
        **user.dict()
    }

@app.post("/production",response_model=productionEntry)
async def register_production(user: productionEntry):
    
    query = production.insert().values(
        name = user.name,
        country = user.country,
        tons_produced = user.tons_produced
        
    )

    await database.execute(query)
    return {
        
        **user.dict()
    }    