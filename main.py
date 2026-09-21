from contextlib import asynccontextmanager
from fastapi import FastAPI
from orm.database import init_db
from routers.books import book_router

@asynccontextmanager
async def lifespan(app:FastAPI):
    await init_db()
    yield


app=FastAPI(title="图书管理API",description="基于 Fastapi+sqlmodel的图书crud接口",
version="1.0.0",
lifespan=lifespan,)

app.include_router(book_router)
@app.get("/",tags=["根路径"])
async def root():
    return {
        "message":"欢迎使用图书管理API",
        "docs":"访问/docs 查看完整接口文档",
        "version":"1.0.0",
    }

if __name__=="__main__":
    import uvicorn
    uvicorn.run("main:app",host="127.0.0.1",port=8000,reload=True)
