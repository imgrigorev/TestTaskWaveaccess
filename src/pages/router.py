from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates

router = APIRouter(
    prefix="/pages",
    tags=["pages"]
)

templates = Jinja2Templates(directory="templates")

@router.get("/base")
def get_base_page(request : Request):
    return templates.TemplateResponse("index.html", {"request":request})