from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class MenuIn(BaseModel):
    """Skema input: id tidak ada di sini, dibuat oleh server."""

    model_config = ConfigDict(str_strip_whitespace=True)

    sku: str = Field(pattern=r"^KOPI-\d{3}$", examples=["KOPI-001"])
    nama: str = Field(min_length=1, max_length=100, examples=["Kopi Susu Gula Aren"])
    kategori: Literal["kopi", "non-kopi", "makanan"]
    harga: int = Field(gt=0, examples=[25000])


class MenuOut(MenuIn):
    """Skema output: input + id yang dibuat server."""

    id: int
