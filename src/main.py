import importlib
import pkgutil
from pathlib import Path

from fastapi import APIRouter, FastAPI

from src.core.config import settings

app = FastAPI(
    title=settings.app_name,
    openapi_url="/openapi.json",
    docs_url="/docs",
    redoc_url="/redoc",
)

api_router = APIRouter()

endpoint_path = Path(__file__).parent / "api" / "endpoints"

templates_dir = Path(__file__).parent / "templates"


for module_info in pkgutil.iter_modules([str(endpoint_path)]):
    if not module_info.ispkg:
        module_name = module_info.name
        full_module_name = f"src.api.endpoints.{module_name}"
        module = importlib.import_module(full_module_name)
        if hasattr(module, "router"):
            api_router.include_router(module.router)
        else:
            raise Exception(f"Модуль {module_name} не имеет роутера.")

app.include_router(api_router, prefix="/api/v1")
