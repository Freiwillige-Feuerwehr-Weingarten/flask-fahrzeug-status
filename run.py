from fastapi import FastAPI, Request, WebSocket, WebSocketDisconnect, BackgroundTasks
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic_settings import BaseSettings, SettingsConfigDict
from datetime import datetime
from functools import lru_cache
from psycopg_pool import AsyncConnectionPool
from contextlib import asynccontextmanager
import psycopg2
import psycopg
import json
import asyncio


class Settings(BaseSettings):
    db_name: str
    db_host: str
    db_user: str
    db_password: str
    db_port: int
    model_config = SettingsConfigDict(env_file='prod.env')
    # TODO: Shall be this
    # model_config = SettingsConfigDict(env_file='prod.env', secrets_dir='')

@lru_cache()
def get_settings():
    return Settings()

class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        print(f"Well hello there")
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)


class RelevantVehicles:
    vehicle_dict = {}
    def __init__(self):
        # TODO: ask the freaking db
        self.vehicle_dict['6145082'] = "50"
        self.vehicle_dict['6145077'] = "10"
        self.vehicle_dict['6145075'] = "191"
        self.vehicle_dict['6145084'] = "23"
        self.vehicle_dict['6145087'] = "33"
        self.vehicle_dict['6145085'] = "441"
        self.vehicle_dict['6145086'] = "442"
        self.vehicle_dict['6145083'] = "52"
        self.vehicle_dict['6145284'] = "591"
        self.vehicle_dict['6145088'] = "73"
        self.vehicle_dict['6145089'] = "56"
        self.vehicle_dict['6145076'] = "192"
        self.vehicle_dict['6145074'] = "10"
        self.vehicle_dict['6145090'] = "100"

ws_manager = ConnectionManager()
settings = get_settings()
app = FastAPI()
templates = Jinja2Templates(directory="templates")
vehicles = RelevantVehicles()

conninfo = f"dbname={settings.db_name} host={settings.db_host} user={settings.db_user} password={settings.db_password} port={settings.db_port}"

def get_conn():
    return psycopg.connect(conninfo=conninfo, autocommit=True)

@lru_cache()
def get_async_pool():
    return AsyncConnectionPool(conninfo=conninfo)

async_pool = get_async_pool()

async def check_async_connection():
    while True:
        await asyncio.sleep(600)
        print("check async connections")
        await async_pool.check()

@asynccontextmanager
async def lifespan(app: FastAPI):
    asyncio.create_task(check_async_connection())
    yield
    pass

async def get_newest_status():
    async with async_pool.connection() as conn:
        await conn.execute("LISTEN status_notification")
        generator = conn.notifies()
        async for notify in generator:
            print(notify)
            splits = notify.payload.strip("()").split(",")
            return splits[0], splits[1]
    return
    # remove below
    with psycopg.Connection.connect(dbname=settings.db_name,
                                                     host=settings.db_host,
                                                     user=settings.db_user,
                                                     password=settings.db_password,
                                                     port=settings.db_port,
                                                     autocommit=True) as aconn:
        aconn.execute("LISTEN status_notification")
        generator = aconn.notifies()
        for notify in generator:
            print(notify)
            splits = notify.payload.strip("()").split(",")
            return splits[0], splits[1]
             

@app.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: int):
    await ws_manager.connect(websocket)
    try:
        while True:
            issi, status = await get_newest_status()
            if issi in vehicles.vehicle_dict:
                new_status = dict(issi=issi, status=status)
                await ws_manager.broadcast(json.dumps(new_status))
            else:
                print(f"Skipping irrelevant vehicle status")
    except WebSocketDisconnect:
        print(f"Client disconnected")
        ws_manager.disconnect(websocket)


def get_vehicle_status(vehicle):
    with get_conn() as connection:
        with connection.cursor() as cursor:
            try:
                cursor.execute("SELECT fahrzeug_status.status FROM fahrzeug_status, fahrzeuge WHERE fahrzeug_status.issi = fahrzeuge.issi AND fahrzeuge.funkrufname = '%s' ORDER BY timestamp DESC LIMIT 1" %vehicle)
            except (Exception, psycopg.DatabaseError) as error:
                return "Nicht bekannt"
            records = cursor.fetchone()

    if not records:
        return "Nicht bekannt"
    else: 
        return records[0]


@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, 
                                                     "status10": get_vehicle_status(10),
                                                     "status11": get_vehicle_status(11),
                                                     "status23": get_vehicle_status(23),
                                                     "status33": get_vehicle_status(33),
                                                     "status441": get_vehicle_status(441),
                                                     "status442": get_vehicle_status(442),
                                                     "status50": get_vehicle_status(50),
                                                     "status52": get_vehicle_status(52),
                                                     "status56": get_vehicle_status(56),
                                                     "status591": get_vehicle_status(591),
                                                     "status73": get_vehicle_status(73),
                                                     "status191": get_vehicle_status(191),
                                                     "status192": get_vehicle_status(192),
                                                     "status100": get_vehicle_status(100)})


@app.get("/status/{vehicle}", response_class=HTMLResponse)
async def status(request: Request, vehicle: str):
    async with async_pool.connection() as conn:
        async with conn.cursor() as cursor:
            await cursor.execute("SELECT * FROM fahrzeug_status, fahrzeuge WHERE fahrzeug_status.issi = fahrzeuge.issi AND fahrzeuge.funkrufname = '%s' ORDER BY timestamp DESC" %vehicle)
            records = await cursor.fetchall()
            return templates.TemplateResponse("fahrzeug.html", {"request": request,
                                                                "vehicle": vehicle,
                                                                "records": records}) 
    connection = psycopg2.connect(database=settings.db_name,
                                  host=settings.db_host,
                                  user=settings.db_user,
                                  password=settings.db_password,
                                  port=settings.db_port)
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM fahrzeug_status, fahrzeuge WHERE fahrzeug_status.issi = fahrzeuge.issi AND fahrzeuge.funkrufname = '%s' ORDER BY timestamp DESC" %vehicle)
    records = cursor.fetchall()
    cursor.close()
    connection.close()
    return templates.TemplateResponse("fahrzeug.html", {"request": request,
                                                     "vehicle": vehicle,
                                                     "records": records}) 


if __name__ == "__main__":
    app.run(host='0.0.0.0, port=5000')
