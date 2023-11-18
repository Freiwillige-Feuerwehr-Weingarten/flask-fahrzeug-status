from fastapi import FastAPI, Request, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.templating import Jinja2Templates
from functools import lru_cache
from contextlib import asynccontextmanager
from app.config import get_settings
from app.db import get_async_pool, get_conn
from app.websocket import get_connection_manager
import psycopg
import json
import asyncio
import uvicorn


ws_manager = get_connection_manager()
settings = get_settings()
async_pool = get_async_pool()
app = FastAPI()
templates = Jinja2Templates(directory="templates")


class RelevantVehicles:
    vehicle_dict = {}
    def __init__(self):
        with get_conn() as conn:
            with conn.cursor() as cursor:
                cursor.execute("SELECT issi, funkrufname FROM fahrzeuge")
                results = cursor.fetchall()
                for row in results:
                    self.vehicle_dict[row[0]] = row[1]

@lru_cache
def get_relevant_vehicles():
    return RelevantVehicles()

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
             

@app.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: int):
    await ws_manager.connect(websocket)
    try:
        while True:
            issi, status = await get_newest_status()
            if issi in get_relevant_vehicles().vehicle_dict:
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
    
def get_latest_vehicles_status() -> dict:
    vehicle_status_dict = dict()
    with get_conn() as connection:
        with connection.cursor() as cursor:
            for issi in get_relevant_vehicles().vehicle_dict: 
                try:
                    cursor.execute("SELECT fahrzeug_status.status FROM fahrzeug_status, fahrzeuge WHERE fahrzeug_status.issi = fahrzeuge.issi AND fahrzeuge.issi = '%s' ORDER BY timestamp DESC LIMIT 1" %issi)
                    r = cursor.fetchone()
                    if not r:
                        vehicle_status_dict[issi] = "Nicht bekannt"
                    else:
                        vehicle_status_dict[issi] = r[0]
                except (Exception, psycopg.DatabaseError) as e:
                    pass
    return vehicle_status_dict


@app.get('/favicon.ico', include_in_schema=False)
async def favicon():
    return FileResponse('favicon.svg')


@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "vdict": get_latest_vehicles_status()})


@app.get("/status/{vehicle}", response_class=HTMLResponse)
async def status(request: Request, vehicle: str):
    async with async_pool.connection() as conn:
        async with conn.cursor() as cursor:
            await cursor.execute("SELECT * FROM fahrzeug_status, fahrzeuge WHERE fahrzeug_status.issi = fahrzeuge.issi AND fahrzeuge.funkrufname = '%s' ORDER BY timestamp DESC" %vehicle)
            records = await cursor.fetchall()
            return templates.TemplateResponse("fahrzeug.html", {"request": request,
                                                                "vehicle": vehicle,
                                                                "records": records}) 


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=5000)
