import fastapi

from fastapi.responses import HTMLResponse
from fastapi.requests import Request
from fastapi.templating import Jinja2Templates
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import exc
from datetime import datetime

from app.database.db_setup import get_async_db
from app.api.utils.status import get_status
from app.api.utils.fahrzeuge import get_radioname_by_issi
from app.pydantic_schemas import status_schema
from app.db import get_async_pool
from app.database.models import status_model

status_router = fastapi.APIRouter()
templates = Jinja2Templates(directory="templates")


@status_router.get("/api/status/", response_model=list[status_schema.Status])
async def aget_status(db: AsyncSession = fastapi.Depends(get_async_db)) -> list[status_schema.Status]:
    status = await get_status(db)
    return status


@status_router.post("/api/status/", response_model=status_schema.Status)
async def handle_post_status(post: status_schema.Status, db: AsyncSession = fastapi.Depends(get_async_db)) -> status_schema.Status:
    new_status = status_model.Status(issi=post.issi,
           status=post.status,
           timestamp=post.timestamp,
           id=post.id)
    try:
        db.add(new_status)
        await db.commit()
        await db.refresh(new_status)
    except exc.IntegrityError:
        raise fastapi.exceptions.HTTPException(status_code=400, detail="Dupclicate Entry")
    return new_status


@status_router.get("/api/status/{issi}", response_model=list[status_schema.Status])
async def aget_status_issi(issi: int, db: AsyncSession = fastapi.Depends(get_async_db)) -> list[status_schema.Status]:
    status = await get_status(db, issi)
    return status


@status_router.get("/status/{issi}", response_class=HTMLResponse)
async def handle_get_status_html(issi: int, request: Request, db: AsyncSession = fastapi.Depends(get_async_db)):
    status_list = await get_status(db, int(issi))
    radio_name = await get_radioname_by_issi(db, int(issi))
    return templates.TemplateResponse("fahrzeug.html", {"request": request,
                                                              "vehicle": radio_name,
                                                              "records": status_list

    })