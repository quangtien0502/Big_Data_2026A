from fastapi import FastAPI
from app.core.config import settings
from app.api.routes import health, road, traffic, weather, statistics

app = FastAPI(
    title=settings.APP_NAME,
    description="Backend for Big Data Integration and Statistical Analysis System",
    version="1.0.0"
)

app.include_router(health.router, prefix="/api/v1/health", tags=["health"])
app.include_router(road.router, prefix="/api/v1/roads", tags=["roads"])
app.include_router(traffic.router, prefix="/api/v1/traffic", tags=["traffic"])
app.include_router(weather.router, prefix="/api/v1/weather", tags=["weather"])
app.include_router(statistics.router, prefix="/api/v1/statistics", tags=["statistics"])

@app.get("/")
def root():
    return {"message": f"Welcome to {settings.APP_NAME}"}

if __name__ == "__main__":
    import uvicorn
    # Lệnh này giúp bạn có thể chạy trực tiếp file main.py bằng nút Play của PyCharm
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
