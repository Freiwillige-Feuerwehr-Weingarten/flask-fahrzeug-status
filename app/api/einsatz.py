import fastapi

from sqlalchemy.ext.asyncio import AsyncSession

from app.database.db_setup import get_async_db
from app.api.utils.einsatz import get_deployments
from app.pydantic_schemas.einsatz import Einsatz

einsatz_router = fastapi.APIRouter()

@einsatz_router.get("/api/deployments/", response_model=list[Einsatz])
async def aget_deployments(db: AsyncSession = fastapi.Depends(get_async_db)) -> list[Einsatz]:
    deployments = await get_deployments(db)
    return deployments

@einsatz_router.post("/api/deployments/")
async def handle_post_deployments(post: Einsatz, db: AsyncSession = fastapi.Depends(get_async_db)) -> Einsatz:
    print(post)
    return post