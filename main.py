from fastapi import FastAPI, HTTPException

from sync import build_result, fetch_orders

app = FastAPI(title="orders-sync")


@app.get("/")
@app.get("/sync")
def sync():
    try:
        orders = fetch_orders()
    except Exception as exc:
        raise HTTPException(status_code=502, detail=f"source unavailable: {exc}")
    return build_result(orders)


@app.get("/health")
def health():
    return {"status": "healthy"}
