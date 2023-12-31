import fastapi

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import exc

from app.database.db_setup import get_async_db
from app.api.utils.einsatz import get_deployments, get_deployment_by_external_data
from app.pydantic_schemas import einsatz_schema
from app.database.models import einsatz_model

einsatz_router = fastapi.APIRouter()


@einsatz_router.get("/api/deployments/", response_model=list[einsatz_schema.Einsatz])
async def aget_deployments(db: AsyncSession = fastapi.Depends(get_async_db)) -> list[einsatz_schema.Einsatz]:
    deployments = await get_deployments(db)
    return deployments


@einsatz_router.post("/api/deployments/")
async def handle_post_deployments(post: einsatz_schema.Einsatz, db: AsyncSession = fastapi.Depends(get_async_db)) -> einsatz_schema.Einsatz:
    print(post)
    new_deployment = einsatz_model.Einsatz(keyword=post.keyword,
                                           keyword_lst=post.keyword_lst,
                                           external_deployment_id=post.external_deployment_id,
                                           external_source=post.external_source,
                                           external_source_id=post.external_source_id,
                                           announcement=post.announcement,
                                           location=post.location,
                                           location_name=post.location_name,
                                           location_info=post.location_info,
                                           location_latitude=post.location_latitude,
                                           location_longitude=post.location_longitude,
                                           # geo_location=post.geo_location,
                                           reporter_name=post.reporter_name,
                                           reporter_info=post.reporter_info,
                                           situation=post.situation,
                                           timestamp_started=post.timestamp_started)
    db.add(new_deployment)
    await db.commit()
    await db.refresh(new_deployment)
    return new_deployment


@einsatz_router.post("/api/deployments/units", response_model=einsatz_schema.Einheit)
async def handle_post_deployments_units(post: einsatz_schema.Einheit, db: AsyncSession = fastapi.Depends(get_async_db)) -> einsatz_schema.Einheit:
    new_unit = einsatz_model.Einheiten(unit=post.unit,
                                       deployment_id=post.deployment_id)
    if not post.deployment_id:
        try:
            deployment = await get_deployment_by_external_data(post.external_source, post.external_deployment_id, db)
        except exc.NoResultFound as excep:
            raise fastapi.exceptions.HTTPException(status_code=400, detail="Deployment doesn't exist") from excep
        except exc.MultipleResultsFound as excep:
            raise fastapi.exceptions.HTTPException(status_code=400, detail="Dataset is ambigous") from excep
        new_unit.deployment_id = deployment.id
    db.add(new_unit)
    await db.commit()
    await db.refresh(new_unit)
    return new_unit
