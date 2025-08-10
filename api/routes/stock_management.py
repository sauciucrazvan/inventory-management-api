from fastapi import APIRouter

router = APIRouter(prefix="/warehouses/{warehouseId}/inventory", tags=["stock_management"])

@router.get("/")
async def get_inventory(warehouseId: int):
    return {"message": f"Inventory list for warehouse {warehouseId}"}

@router.get("/{productId}")
async def get_product_inventory(warehouseId: int, productId: int):
    return {"message": f"Inventory details for product {productId} in warehouse {warehouseId}"}

@router.post("/{productId}/increase")
async def increase_product_inventory(warehouseId: int, productId: int):
    return {"message": f"Increased inventory for product {productId} in warehouse {warehouseId}"}

@router.post("/{productId}/decrease")
async def decrease_product_inventory(warehouseId: int, productId: int):
    return {"message": f"Decreased inventory for product {productId} in warehouse {warehouseId}"}

@router.post("/{productId}/transfer")
async def transfer_product_inventory(warehouseId: int, productId: int):
    return {"message": f"Transferred inventory for product {productId} in warehouse {warehouseId}"}
