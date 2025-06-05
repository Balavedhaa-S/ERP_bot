from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from typing import List, Dict

async def run_sql_query(db: AsyncSession, sql: str) -> List[Dict]:
    result = await db.execute(text(sql))
    rows = result.fetchall()
    return [dict(row._mapping) for row in rows]

