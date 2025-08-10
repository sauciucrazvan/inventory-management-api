from fastapi import APIRouter

router = APIRouter(prefix="/warehouses/{warehouseId}/products", tags=["product_management"])

@router.post("/")
async def create_product(warehouseId: int):
    return {"message": f"Product created in warehouse {warehouseId}"}

@router.get("/")
async def get_products(warehouseId: int):
    return {"message": f"List of products in warehouse {warehouseId}"}

@router.get("/{id}")
async def get_product(warehouseId: int, id: int):
    return {"message": f"Product {id} details in warehouse {warehouseId}"}

@router.patch("/{id}")
async def patch_product(warehouseId: int, id: int):
    return {"message": f"Product {id} partially updated in warehouse {warehouseId}"}

@router.put("/{id}")
async def update_product(warehouseId: int, id: int):
    return {"message": f"Product {id} fully updated in warehouse {warehouseId}"}

@router.delete("/{id}")
async def delete_product(warehouseId: int, id: int):
    return {"message": f"Product {id} deleted from warehouse {warehouseId}"}
