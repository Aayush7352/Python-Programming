"""
FastAPI web application demonstration.

Requires: pip install fastapi uvicorn
"""
import sys
import time


def main():
    """FastAPI demo with automatic OpenAPI docs."""
    try:
        from fastapi import FastAPI, HTTPException, Query, Path
        from pydantic import BaseModel, Field
        import uvicorn
    except ImportError:
        print("FastAPI/uvicorn not installed.")
        print("Install with: pip install fastapi uvicorn")
        sys.exit(1)

    app = FastAPI(
        title="FastAPI Demo API",
        version="1.0.0",
        description="Demonstration of FastAPI features",
    )

    # Pydantic models
    class Item(BaseModel):
        name: str = Field(..., min_length=1, max_length=100)
        price: float = Field(..., gt=0)
        description: str | None = Field(None, max_length=500)
        tax: float = Field(0, ge=0)

    class ItemResponse(BaseModel):
        id: int
        name: str
        price: float
        description: str | None
        tax: float
        total_price: float

    class UpdateItem(BaseModel):
        name: str | None = None
        price: float | None = Field(None, gt=0)
        description: str | None = None
        tax: float | None = Field(None, ge=0)

    # In-memory storage
    items = {}
    next_id = 1

    @app.get("/")
    async def root():
        return {
            "app": "FastAPI Demo",
            "docs": "/docs",
            "openapi": "/openapi.json",
        }

    @app.get("/items", response_model=list[ItemResponse])
    async def list_items(
        skip: int = Query(0, ge=0),
        limit: int = Query(10, ge=1, le=100),
        min_price: float | None = Query(None, ge=0),
    ):
        result = []
        for item_id, item in items.items():
            if min_price is not None and item["price"] < min_price:
                continue
            if skip > 0:
                skip -= 1
                continue
            if len(result) >= limit:
                break
            result.append(ItemResponse(id=item_id, **item))
        return result

    @app.get("/items/{item_id}", response_model=ItemResponse)
    async def get_item(
        item_id: int = Path(..., ge=1, description="Item ID")
    ):
        if item_id not in items:
            raise HTTPException(status_code=404, detail=f"Item {item_id} not found")
        item = items[item_id]
        return ItemResponse(id=item_id, **item)

    @app.post("/items", response_model=ItemResponse, status_code=201)
    async def create_item(item: Item):
        nonlocal next_id
        item_data = item.model_dump()
        total_price = item_data["price"] + item_data["tax"]
        items[next_id] = {**item_data, "total_price": total_price}
        response = ItemResponse(id=next_id, **items[next_id])
        next_id += 1
        return response

    @app.put("/items/{item_id}", response_model=ItemResponse)
    async def update_item(item_id: int, item: UpdateItem):
        if item_id not in items:
            raise HTTPException(status_code=404, detail=f"Item {item_id} not found")

        current = items[item_id]
        update_data = item.model_dump(exclude_none=True)
        current.update(update_data)

        price = current.get("price", 0)
        tax = current.get("tax", 0)
        current["total_price"] = price + tax

        items[item_id] = current
        return ItemResponse(id=item_id, **current)

    @app.delete("/items/{item_id}")
    async def delete_item(item_id: int):
        if item_id not in items:
            raise HTTPException(status_code=404, detail="Item not found")
        del items[item_id]
        return {"message": "Item deleted", "id": item_id}

    @app.get("/items/count/")
    async def item_count():
        return {"count": len(items)}

    @app.get("/health")
    async def health():
        return {
            "status": "healthy",
            "timestamp": time.time(),
            "items_count": len(items),
        }

    print("=== FastAPI Demo ===")
    print("  This file defines a FastAPI application.")
    print("  Run with: uvicorn 67_fastapi:app --reload")
    print("  Or programmatically:")

    print("\n  Starting FastAPI test server on http://127.0.0.1:8000")
    print("  API Docs: http://127.0.0.1:8000/docs")
    print("  Press Ctrl+C to stop\n")

    import threading
    server = threading.Thread(
        target=uvicorn.run,
        args=(app,),
        kwargs={"host": "127.0.0.1", "port": 8000, "log_level": "error"},
        daemon=True
    )
    server.start()

    import time
    time.sleep(2)

    # Test the API
    import httpx
    try:
        r = httpx.get("http://127.0.0.1:8000/")
        print(f"  GET /: {r.json()}")

        r = httpx.post(
            "http://127.0.0.1:8000/items",
            json={"name": "Laptop", "price": 999.99, "tax": 50.0}
        )
        print(f"  POST /items: {r.json()}")

        r = httpx.get("http://127.0.0.1:8000/items/1")
        print(f"  GET /items/1: {r.json()}")

        print("\n  Server running. Try:")
        print("    curl http://127.0.0.1:8000/docs")
        print("    curl http://127.0.0.1:8000/openapi.json")

    except Exception as e:
        print(f"  Test error: {e}")

    print("\n  (Server stops when script exits)")


if __name__ == "__main__":
    main()
