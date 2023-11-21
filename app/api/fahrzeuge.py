import fastapi

from sqlalchemy.ext.asyncio import AsyncSession

from app.database.db_setup import get_async_db
from app.api.utils.fahrzeuge import get_vehicles
from app.pydantic_schemas.fahrzeuge import Fahrzeuge

fahrzeuge_router = fastapi.APIRouter()

@fahrzeuge_router.get("/vehicles/", response_model=list[Fahrzeuge])
async def aget_vehicles(db: AsyncSession = fastapi.Depends(get_async_db)) -> list[Fahrzeuge]:
    vehicles = await get_vehicles(db)
    return vehicles

@fahrzeuge_router.post("/vehicles/")
async def apost_vehicles(post: Fahrzeuge) -> Fahrzeuge:
    return post
