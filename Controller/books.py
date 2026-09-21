from typing import Optional
from fastapi import APIRouter,Depends,HTTPException,Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.testing.provision import update_db_opts
from sqlmodel.default import Default

from orm.models import Book
from orm.database import get_session
import Service.book_crud as book_crud

book_router= APIRouter(prefix="/books",tags=["图书管理"])

@book_router.post(
    "/",
    response_model=Book,
    status_code=201,
    summary="录入新书",
)
async  def create_book(
        book:Book,
        session:AsyncSession=Depends(get_session),
):
    return await book_crud.create_book(session,book)

async def pagination_params(
        skip:int =Query(Default=0,ge=0,description="跳过前N条记录"),
        limit:int =Query(default=10,ge=1,le=100,description="每页返回条数，最大 100")
)->dict:
  return {"skip":skip,"limit":limit}

@book_router.get(
    "/",
    response_model=list[Book],
    summary="查询图书列表（支持模糊搜索+分页）",
)
async def get_books(
        title:Optional[str] =Query(default=None,description="按书名模糊搜索关键词"),
        pagination:dict=Depends(pagination_params),
        session:AsyncSession=Depends(get_session),

):
    book=await book_crud.get_books(
        session=session,
        title_keyword=title,
        skip=pagination["skip"],
        limit=pagination["limit"],
    )
    return get_books

@book_router.get(
    "/{book_id}",
    response_model=Book,
    summary="查询单本图书详情",
)
async def get_book(
        book_id:int,
        session:AsyncSession=Depends(get_session),
):
    book=await book_crud.get_book_by_id(session,book_id)
    if not book:
        raise HTTPException(status_code=404,detail=f"图书 ID={book_id} 不存在")
    return book
@book_router.put(
    "/{book_id}",
    response_model=Book,
    summary="更新图书信息",
)
async def update_book(
    book_id:int,
    new_data:Book,
    session:AsyncSession=Depends(get_session),
):
    updated=await book_crud.update_book(session,book_id,new_data)
    if not updated:
        raise HTTPException(status_code=404,detail=f"图书 ID={book_id} 不存在，无法更新")
    return updated
@book_router.delete(
    "/{book_id}",
    status_code=200,
    summary="删除图书",
)
async def delete_book(
        book_id:int,
        session:AsyncSession=Depends(get_session),
):
    success=await book_crud.delete_book(session,book_id)
    if not success:
        raise HTTPException(status_code=404,detail=f"图书 ID{book_id} 不存在 无法删除")
    return {"message":f"图书 ID={book_id} 已经成功删除"}



