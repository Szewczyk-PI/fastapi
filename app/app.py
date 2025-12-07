from fastapi import FastAPI, HTTPException
from app.scheamas import PostCreate, PostReturn
from app.db import Post, create_db_and_tables, get_async_session 
from sqlalchemy.ext.asyncio import AsyncSession
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_db_and_tables()
    yield

app = FastAPI(lifespan=lifespan)

text_post = {1: {"title": "New Post", "content": "Cool New Post"},
             2: {"title": "Recenzja Filmu 'Gwiezdny Pył'", "content": "Wzruszająca opowieść fantasy z zaskakującymi zwrotami akcji"}, 
             3: {"title": "Przepisy na wege obiady", "content": "Dziś proponujemy szybkie curry z ciecierzycą i batatami."}, 
             4: {"title": "Raport Kwartalny Q3 2025", "content": "Wzrost przychodów o 15% w porównaniu do poprzedniego kwartału."}, 
             5: {"title": "Ogłoszenie: Spotkanie Zespołu", "content": "Spotkanie dotyczące harmonogramu projektu odbędzie się w poniedziałek o 10:00."}, 
             6: {"title": "Wskazówki Dotyczące SEO", "content": "Pamiętaj o optymalizacji meta tagów i budowaniu naturalnych linków zwrotnych."}}

@app.get("/posts")
def get_all_posts(limit: int = None):
    if limit:
        return list(text_post.values())[:limit]
    return text_post

@app.get("/posts/{id}")
def get_post_id(id: int) -> PostReturn:
    if id not in text_post:
        raise HTTPException(status_code=404,detail="ID not found")
    return text_post.get(id)

@app.post("/posts")
def create_post(post: PostCreate) -> PostReturn: 
    new_post = {"title": post.title, "content": post.content}
    text_post[max(text_post.keys()) + 1 ] = new_post
    return new_post