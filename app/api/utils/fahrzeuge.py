from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.database.models.fahrzeuge import Fahrzeuge

async def get_vehicles(db: AsyncSession):
    query = select(Fahrzeuge)
    result = await db.execute(query)
    return result.scalars().all()