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

@fahrzeuge_router.post("/vehicles/", response_model=Fahrzeuge)
async def apost_vehicles(post: Fahrzeuge, db: AsyncSession = fastapi.Depends(get_async_db)) -> Fahrzeuge:
    new_vehicle = Fahrzeuge(issi=post.issi,
                            funkrufname=post.funkrufname)
    db.add(new_vehicle)
    await db.commit
    await db.refresh(new_vehicle)
    return new_vehicle
