from fastapi import FastAPI

app=FastAPI(title="Product API", description="API for managing products", version="1.0.0")

@app.get("/health", tags=["system"])
async def health_check():
    return {"status": "healthy"}
