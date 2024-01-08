from contextlib import AbstractAsyncContextManager
from typing import Callable

from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.schema.news import News
from app.errors import exceptions as ex


class NewsListRepository:
    def __init__(self, session_factory: Callable[..., AbstractAsyncContextManager[AsyncSession]]) -> None:
        self.session_factory = session_factory

    async def get_news_list_repository(self) -> list[dict] | None:
        """
        뉴스 리스트 Repository
        """
        try:
            async with self.session_factory() as session:
                result = await session.scalars(select(News))
                news_list = result.all()
                if news_list is None:
                    return None
                return [
                    {
                        "article_id": news.article_id,
                        "title": news.title,
                        "source": news.source,
                        "user_number": news.user_number,
                        "url": news.url,
                    }
                    for news in news_list
                ]
        except SQLAlchemyError as e:
            raise ex.InternalQuerryEx(ex=e)