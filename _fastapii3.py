from fastapi import FastAPI
import sqlalchemy as sal
import json

app = FastAPI()

def connectiondb():
    with open("config.json","r") as file:
        config = json.load(file)

    user=config["user"]
    password=config["password"]
    host=config["host"]
    database=config["database"]
    driver = config["driver"]
    
    conn_str = f"mssql+pyodbc://{user}:{password}@{host}/{database}?driver={driver}"
    engine = sal.create_engine(url=conn_str)
    return engine

def select_query():
    data_list = []
    engine = connectiondb()
    with engine.connect() as connectionn:
        result = connectionn.execute(sal.text("Select * from tbl_todo"))
        for row in result:
            data_list.append( {"id":row[0], "mesaj":row[1]} )
    return data_list


def insert_query(id:int,message:str):
    engine = connectiondb()
    with engine.connect() as connectionn:
        connectionn.execute(sal.text("INSERT INTO tbl_todo values (:val1, :val2) "), {"val1":id,"val2":message})
        connectionn.commit()
        return "kayit eklendi"


def delete_query(id:int):
    engine = connectiondb()
    with engine.connect() as connectionn:
        result = connectionn.execute(sal.text("SELECT * FROM tbl_todo where id= :val1"),{"val1":id})
        
        if result.fetchone() is not None :
            connectionn.execute(sal.text("DELETE FROM tbl_todo where id= :val1"),{"val1":id})
            connectionn.commit()
            return "kayıt silindi."
        else:
            return "kayıt bulunamadı."


def update_query(id:int,message:str):
    engine = connectiondb()
    with engine.connect() as connectionn:
        result = connectionn.execute(sal.text("SELECT * FROM tbl_todo where id= :val1"),{"val1":id})
        if result.fetchone() is not None:
            connectionn.execute(sal.text("UPDATE tbl_todo SET message= :val1 WHERE id= :val2"),{"val1":message,"val2":id})
            connectionn.commit()
            return "kayıt güncellendi"
        else:
            return "kayıt bulunamadı"


@app.get('/todos/')
async def get_todos():
    return {"todos":select_query()}

@app.post('/todos/')
async def post_todos(id:int,message:str):
    return insert_query(id,message)


@app.delete('/todos/')
async def delete_todos(id:int):
    return delete_query(id)

@app.put('/todos/')
async def update_todos(id:int,message:str):
    return update_query(id,message)
