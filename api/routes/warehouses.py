from fastapi import APIRouter

router = APIRouter(prefix="/warehouses", tags=["warehouses"])

@router.post("/")
async def create_warehouse():
    return {"message": "Warehouse created"}

@router.get("/")
async def get_warehouses():
    return {"message": "List of warehouses"}

@router.get("/{id}")
async def get_warehouse(id: int):
    return {"message": f"Warehouse {id} details"}

@router.patch("/{id}")
async def patch_warehouse(id: int):
    return {"message": f"Warehouse {id} partially updated"}

@router.put("/{id}")
async def update_warehouse(id: int):
    return {"message": f"Warehouse {id} fully updated"}
