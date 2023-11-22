import fastapi

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import exc

from app.database.db_setup import get_async_db
from app.database.models import fahrzeuge_model
from app.api.utils.fahrzeuge import get_vehicles
from app.pydantic_schemas import fahrzeuge_schema

fahrzeuge_router = fastapi.APIRouter()

@fahrzeuge_router.get("/api/vehicles/", response_model=list[fahrzeuge_schema.Fahrzeuge])
async def handle_get_vehicles(db: AsyncSession = fastapi.Depends(get_async_db)) -> list[fahrzeuge_schema.Fahrzeuge]:
    vehicles = await get_vehicles(db)
    return vehicles

@fahrzeuge_router.post("/api/vehicles/", response_model=fahrzeuge_schema.Fahrzeuge, status_code=fastapi.status.HTTP_201_CREATED)
async def handle_post_vehicles(post: fahrzeuge_schema.Fahrzeuge, db: AsyncSession = fastapi.Depends(get_async_db)) -> fahrzeuge_schema.Fahrzeuge:
    new_vehicle = fahrzeuge_model.Fahrzeuge(issi=post.issi,
                            funkrufname=post.funkrufname)
    try:
        db.add(new_vehicle)
        await db.commit()
        await db.refresh(new_vehicle)
    except exc.IntegrityError:
        raise fastapi.exceptions.HTTPException(status_code=400, detail="Dupclicate Entry")
    return new_vehicle
