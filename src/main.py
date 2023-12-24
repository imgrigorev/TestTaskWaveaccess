from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from pages.router import router as router_pages
from auth.router import router as router_auth
from tasks.router import router as router_task


app = FastAPI(
    docs_url="/",
    title="Tasktracker"
)

app.mount("/static", StaticFiles(directory="static"), name="static")


app.include_router(router_task)
app.include_router(router_pages)
app.include_router(router_auth)
