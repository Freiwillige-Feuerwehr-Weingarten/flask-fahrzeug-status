from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.database.models import einsatz_model

async def get_deployments(db: AsyncSession):
    query = select(einsatz_model.Einsatz)
    result = await db.execute(query)
    return result.scalars().all()

async def get_deployment_by_external_data(external_source: str, external_deployment_id: int, db: AsyncSession) -> einsatz_model.Einsatz:
    query = select(einsatz_model.Einsatz).where(einsatz_model.Einsatz.external_deployment_id == external_deployment_id,
                                                einsatz_model.Einsatz.external_source == external_source)
    result = await db.execute(query)
    return result.scalar_one()