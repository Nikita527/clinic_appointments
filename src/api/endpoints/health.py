from fastapi import APIRouter

router = APIRouter(prefix="/health", tags=["Проверка работоспособности"])


@router.get("")
async def health() -> dict[str, str]:
    return {"status": "ok"}
