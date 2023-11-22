from fastapi import FastAPI, Request, WebSocket, WebSocketException
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.templating import Jinja2Templates
from functools import lru_cache
from contextlib import asynccontextmanager
from app.config import get_settings
from app.db import get_async_pool, get_conn
from app.websocket import get_connection_manager
from app.database import db_setup
from app.api.fahrzeuge import fahrzeuge_router
from app.api.status import status_router
from app.api.einsatz import einsatz_router
from app.database.models import einsatz_model, fahrzeuge_model, status_model
from app.api.utils.status import get_latest_vehicles_status, get_relevant_vehicles, RelevantVehicles
# from pydantic import BaseModel
# import psycopg
import sys
import json
import asyncio
import uvicorn

@asynccontextmanager
async def lifespan(app: FastAPI):
    asyncio.create_task(check_async_connection())
    print("In contextmanager")
    # TODO: remove
    sys.dont_write_bytecode = True
    await async_pool.open()
    async with db_setup.async_engine.begin() as aconn:
        await aconn.run_sync(fahrzeuge_model.Base.metadata.create_all)
        await aconn.run_sync(status_model.Base.metadata.create_all)
        await aconn.run_sync(einsatz_model.Base.metadata.create_all)
    yield
    pass

ws_manager = get_connection_manager()
settings = get_settings()
async_pool = get_async_pool()
app = FastAPI(
    title="Fahrzeug Status",
    version="0.0.1",
    contact={
        "email": "admin@ff-weingarten.de",
    },
    license_info={
        "name": "MIT",
    },
    lifespan=lifespan)
app.include_router(fahrzeuge_router)
app.include_router(status_router)
app.include_router(einsatz_router)
templates = Jinja2Templates(directory="templates")


async def check_async_connection():
    while True:
        await asyncio.sleep(600)
        print("check async connections")
        await async_pool.check()


async def get_newest_status():
    async with async_pool.connection() as conn:
        print(f"Awaiting LISTEN status_notification")
        await conn.set_autocommit(True)
        await conn.execute("LISTEN status_notification")
        print(f"Notification received")
        async for notify in conn.notifies():
            print(notify)
            splits = notify.payload.strip("()").split(",")
            return splits[0], splits[1]
             

@app.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: int):
    await ws_manager.connect(websocket)
    try:
        while True:
            print(get_relevant_vehicles().vehicle_dict)
            issi, status = await get_newest_status()
            print(f"Issi {issi}, Status {status}")
            vehicles = get_relevant_vehicles().vehicle_dict
            if int(issi) in vehicles:
                new_status = dict(issi=issi, status=status)
                await ws_manager.broadcast(json.dumps(new_status))
            else:
                print(f"Skipping irrelevant vehicle status")
    except WebSocketException:
        # TODO: Could also get psycopg.OperatoinalError
        print(f"Client {client_id} disconnected")
        ws_manager.disconnect(websocket)


@app.get('/favicon.ico', include_in_schema=False)
async def favicon():
    return FileResponse('favicon.svg')


@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request,
                                                     "vdict": get_latest_vehicles_status(),
                                                     "server_hostname": settings.server_hostname,
                                                     "server_port": settings.server_port})


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=5000)
