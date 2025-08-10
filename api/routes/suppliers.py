from fastapi import APIRouter

router = APIRouter(prefix="/suppliers", tags=["suppliers"])

@router.post("/")
async def create_supplier():
    return {"message": "Supplier created"}

@router.get("/")
async def get_suppliers():
    return {"message": "List of suppliers"}

@router.get("/{id}")
async def get_supplier(id: int):
    return {"message": f"Supplier {id} details"}

@router.patch("/{id}")
async def patch_supplier(id: int):
    return {"message": f"Supplier {id} partially updated"}

@router.put("/{id}")
async def update_supplier(id: int):
    return {"message": f"Supplier {id} fully updated"}
