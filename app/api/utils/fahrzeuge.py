from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from ...database.models import fahrzeuge_model


async def get_vehicles(db: AsyncSession):
    query = select(fahrzeuge_model.Fahrzeuge)
    result = await db.execute(query)
    return result.scalars().all()

async def get_radioname_by_issi(db: AsyncSession, issi: int):
    query = select(fahrzeuge_model.Fahrzeuge).where(fahrzeuge_model.Fahrzeuge.issi == issi)
    result = await db.execute(query)
    return result.scalar_one_or_none()