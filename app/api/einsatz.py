import fastapi

from sqlalchemy.ext.asyncio import AsyncSession

from app.database.db_setup import get_async_db
from app.api.utils.einsatz import get_deployments
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
                                           external_deployment_id=post.external_deployment_id,
                                           external_source=post.external_source,
                                           external_source_id=post.external_source_id,
                                           announcement=post.announcement,
                                           location=post.location,
                                           location_name=post.location_name,
                                           location_info=post.location_info,
                                           reporter_name=post.reporter_name,
                                           repoter_info=post.repoter_info,
                                           situation=post.situation,
                                           timestamp_started=post.timestamp_started)
    #TODO: there a typo in "repoter_info"
    db.add(new_deployment)
    await db.commit()
    await db.refresh(new_deployment)
    return new_deployment