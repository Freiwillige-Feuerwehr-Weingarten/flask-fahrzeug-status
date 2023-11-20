import fastapi

from fastapi.responses import HTMLResponse
from fastapi.requests import Request
from fastapi.templating import Jinja2Templates
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.db_setup import get_async_db
from app.api.utils.status import get_status
from app.pydantic_schemas.status import Status
from app.db import get_async_pool

status_router = fastapi.APIRouter()
templates = Jinja2Templates(directory="templates")

@status_router.get("/api/status/", response_model=list[Status])
async def aget_status(db: AsyncSession = fastapi.Depends(get_async_db)) -> list[Status]:
    status = await get_status(db)
    return status


@status_router.get("/api/status/{issi}", response_model=list[Status])
async def aget_status_issi(issi: int, db: AsyncSession = fastapi.Depends(get_async_db)) -> list[Status]:
    status = await get_status(db, issi)
    return status


@status_router.get("/status/{vehicle}", response_class=HTMLResponse)
async def aafahrzeug_status(request: Request, vehicle: str):
    async with get_async_pool().connection() as conn:
        async with conn.cursor() as cursor:
            await cursor.execute("SELECT * FROM fahrzeug_status, fahrzeuge WHERE fahrzeug_status.issi = fahrzeuge.issi AND fahrzeuge.funkrufname = '%s' ORDER BY timestamp DESC" %vehicle)
            records = await cursor.fetchall()
            return templates.TemplateResponse("fahrzeug.html", {"request": request,
                                                                "vehicle": vehicle,
                                                                "records": records}) 