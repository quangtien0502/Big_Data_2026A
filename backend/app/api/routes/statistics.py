from fastapi import APIRouter

router = APIRouter()

@router.get("/traffic")
def get_traffic_statistics():
    return {"message": "Not implemented yet"}

@router.get("/anomalies")
def get_anomalies():
    return {"message": "Not implemented yet"}
