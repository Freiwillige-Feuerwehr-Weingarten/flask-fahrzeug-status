import psycopg

from functools import lru_cache
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.database.models.status import Status
from app.db import get_conn

async def get_status(db: AsyncSession, issi: int = 0):
    if issi:
        query = select(Status).where(Status.issi== issi)
    else:
        query = select(Status)
    result = await db.execute(query)
    return result.scalars().all()

def get_latest_vehicles_status() -> dict:
    vehicle_status_dict = dict()
    with get_conn() as connection:
        with connection.cursor() as cursor:
            for issi in get_relevant_vehicles().vehicle_dict: 
                try:
                    cursor.execute("SELECT fahrzeug_status.status FROM fahrzeug_status, fahrzeuge WHERE fahrzeug_status.issi = fahrzeuge.issi AND fahrzeuge.issi = '%s' ORDER BY timestamp DESC LIMIT 1" %issi)
                    r = cursor.fetchone()
                    if not r:
                        vehicle_status_dict[issi] = "Nicht bekannt"
                    else:
                        vehicle_status_dict[issi] = r[0]
                except (Exception, psycopg.DatabaseError) as e:
                    pass
    return vehicle_status_dict


class RelevantVehicles:
    vehicle_dict = {}
    def __init__(self):
        with get_conn() as conn:
            with conn.cursor() as cursor:
                cursor.execute("SELECT issi, funkrufname FROM fahrzeuge")
                results = cursor.fetchall()
                for row in results:
                    self.vehicle_dict[row[0]] = row[1]

@lru_cache
def get_relevant_vehicles() -> RelevantVehicles:
    return RelevantVehicles()