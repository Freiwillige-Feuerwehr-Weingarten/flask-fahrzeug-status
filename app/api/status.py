import fastapi

from sqlalchemy.ext.asyncio import AsyncSession

from app.database.db_setup import get_async_db
from app.api.utils.status import get_status
from app.pydantic_schemas.status import Status

status_router = fastapi.APIRouter()

@status_router.get("/status/", response_model=list[Status])
async def aget_status(db: AsyncSession = fastapi.Depends(get_async_db)) -> list[Status]:
    status = await get_status(db)
    return status
