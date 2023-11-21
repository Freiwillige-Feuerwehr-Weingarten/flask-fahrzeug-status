from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.database.models.fahrzeuge import Fahrzeuge


async def get_vehicles(db: AsyncSession):
    query = select(Fahrzeuge)
    result = await db.execute(query)
    return result.scalars().all()

async def get_radioname_by_issi(db: AsyncSession, issi: int):
    query = select(Fahrzeuge).where(Fahrzeuge.issi == issi)
    result = await db.execute(query)
    return result.scalar_one_or_none()