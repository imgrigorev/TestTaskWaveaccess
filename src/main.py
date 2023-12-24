from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from pages.router import router as router_pages
from auth.router import router as router_auth
from tasks.router import router as router_task

description = """
BagTraker. 🚀

## Tasks

You can **read tasks**.

You can **create tasks**.

You can **update tasks**.

You can **delete tasks, if u are admin**.

## Auth - Authentication

You will be able to:

* **Authenticate** 
* **Sign in** 
* **Sign up** 

If you are admin:
* You can **change user`s role**
* You can **change user`s login**

How to use:
First of all - u need to sign in, next you will get token and can do all the staff

"""

app = FastAPI(
    docs_url="/",
    title="Tasktracker",
    description=description,
    version="0.0.1",
    contact={
        "url": "http://t.me/imgrigorev",
    },
    license_info={
        "name": "Apache 2.0",
        "url": "https://www.apache.org/licenses/LICENSE-2.0.html",
    },
)

app.mount("/static", StaticFiles(directory="static"), name="static")


app.include_router(router_task)
app.include_router(router_pages)
app.include_router(router_auth)
