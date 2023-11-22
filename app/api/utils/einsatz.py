from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.database.models import einsatz_model

async def get_deployments(db: AsyncSession):
    query = select(einsatz_model.Einsatz)
    result = await db.execute(query)
    return result.scalars().all()
