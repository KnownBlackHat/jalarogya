from datetime import datetime

from pymongo.collection import Collection


def insert_alert(message: str, collection: Collection) -> bool:

    alert = {
        "message": message,
        "timestamp": datetime.utcnow(),
    }
    result = collection.insert_one(alert)
    return result.acknowledged


def get_alert(collection: Collection, limit: int = 10) -> list[dict]:
    alerts = collection.find().sort("timestamp", -1).limit(limit)
    return list(alerts)
