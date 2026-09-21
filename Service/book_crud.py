from datetime import date
from typing import Optional
from sqlmodel import select
from sqlalchemy.ext.asyncio import  AsyncSession
from  orm.models import Book

async def create_book(session:AsyncSession,book:Book)->Book:
    if isinstance(book.publish_date,str):
        book.publish_date = date.fromisoformat(book.publish_date)
    session.add(book)
    await session.commit()
    await session.refresh(book)
    return book

async def get_books(
        session:AsyncSession,
        title_keyword:Optional[str],
        skip:int,
        limit:int,
) -> list[Book]:
    statement=select(Book)
    if title_keyword:
        statement=statement.where(Book.title.contains(title_keyword))
    statement=statement.offset(skip).limit
    result =await session.execute(statement)

    return result.scalars().all()

async def get_book_by_id(session:AsyncSession,book_id:int) ->Optional[Book]:
    return await session.get(Book,book_id)

async def update_book(
        session:AsyncSession,
        book_id:int,
        new_data:Book,
)->Optional[Book]:
    book=await session.get(Book,book_id)
    if not book:
        return None

    book.title=new_data.title
    book.author=new_data.author
    book.price=new_data.price

    if new_data.publish_data is not None:
        if isinstance(new_data.publish_data,str):
            book.publish_data=date.fromisoformat(new_data.publish_data)
        if new_data.description is not None:
            book.description=new_data.description
        session.add(book)
        await session.commit()
        await session.refresh(book)
        return book
async def delete_book(session:AsyncSession,book_id: int) ->bool:
    book= await session.get(Book,book_id)
    if not book:
        return False
    await session.delete(book)
    await session.commit()
    return True
