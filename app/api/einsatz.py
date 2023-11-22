import fastapi

from sqlalchemy.ext.asyncio import AsyncSession

from app.database.db_setup import get_async_db
from app.api.utils.einsatz import get_deployments
from app.pydantic_schemas import einsatz_schema

einsatz_router = fastapi.APIRouter()

@einsatz_router.get("/api/deployments/", response_model=list[einsatz_schema.Einsatz])
async def aget_deployments(db: AsyncSession = fastapi.Depends(get_async_db)) -> list[einsatz_schema.Einsatz]:
    deployments = await get_deployments(db)
    return deployments

@einsatz_router.post("/api/deployments/")
async def handle_post_deployments(post: einsatz_schema.Einsatz, db: AsyncSession = fastapi.Depends(get_async_db)) -> einsatz_schema.Einsatz:
    print(post)
    return post