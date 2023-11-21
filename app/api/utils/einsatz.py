from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.database.models.einsatz import Einsatz

async def get_deployments(db: AsyncSession):
    query = select(Einsatz)
    result = await db.execute(query)
    return result.scalars().all()