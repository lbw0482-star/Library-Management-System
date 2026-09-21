from typing import Optional
from datetime import date
from sqlmodel import SQLModel,Field

class Book (SQLModel,table=True):
    id:Optional[int] = Field(
        default=None,
        primary_key=True,
        description="图书唯一 ID （自增主键）"
    )

    title:str =Field(
        index=True,
        nullable=False,
        max_length=200,
        description="图书标题"
    )

    author:str=Field(
        nullable=False,
        max_length=100,
        description="作者姓名"
    )

    publish_data:Optional[date]=Field(
        default=None,
        description="出版日期，格式 YYYY-MM-DD"
    )

    price:float=Field(
        gt=0,
        description="图书定价（元），必须大于0"
    )

    description:Optional[str]=Field(
        default=None,
        max_length=1000,
        description="图书简介"
    )