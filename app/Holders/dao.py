from sqlalchemy import select
from sqlalchemy.orm import load_only

from app.dao.base import BaseDAO
from app.database import gen_session
from app.Holders.models import Holders


class HoldersDAO(BaseDAO):
    model = Holders

    @classmethod
    async def all_mails(cls):
        async with gen_session() as session:
            q = select(Holders.email).distinct()
            r = await session.execute(q)
            # return [row[0].email for row in r.scalars().all()]
            return r.scalars().all()
