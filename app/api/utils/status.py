from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.database.models.status import Status

async def get_status(db: AsyncSession):
    query = select(Status)
    result = await db.execute(query)
    return result.scalars().all()