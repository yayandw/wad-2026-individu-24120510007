from fastapi import APIRouter, HTTPException, Query, Response, status

from app.schemas import MenuIn, MenuOut

router = APIRouter(prefix="/api/menu", tags=["menu"])

# Penyimpanan sementara di memori (SQLite/Postgres baru masuk di sesi berikutnya).
_db: dict[int, MenuOut] = {}
_next_id = 1


def reset_store() -> None:
    global _next_id
    _db.clear()
    _next_id = 1


@router.post("", response_model=MenuOut, status_code=status.HTTP_201_CREATED)
def create_menu(payload: MenuIn, response: Response):
    global _next_id
    if any(m.sku == payload.sku for m in _db.values()):
        raise HTTPException(status.HTTP_409_CONFLICT, f"SKU {payload.sku} sudah dipakai")
    item = MenuOut(id=_next_id, **payload.model_dump())
    _db[item.id] = item
    _next_id += 1
    response.headers["Location"] = f"/api/menu/{item.id}"
    return item


@router.get("", response_model=list[MenuOut])
def list_menu(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    search: str | None = Query(None, description="Cari di nama atau SKU"),
):
    items = list(_db.values())
    if search:
        q = search.lower()
        items = [m for m in items if q in m.nama.lower() or q in m.sku.lower()]
    return items[skip : skip + limit]


@router.get("/{menu_id}", response_model=MenuOut)
def get_menu(menu_id: int):
    item = _db.get(menu_id)
    if item is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Menu tidak ditemukan")
    return item
