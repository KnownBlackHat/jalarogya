from pymongo.collection import Collection

from models.heatmap import HeatMap


def insert_heatmap(data: HeatMap, collection: Collection) -> bool:
    result = collection.find_one_and_update(
        {"city": data.city},
        {
            "$inc": {"count": data.count},
            "$set": {
                "severity": data.severity,
                "latitude": data.latitude,
                "longitude": data.longitude,
            },
        },
        upsert=True,
    )
    return result.acknowledged


def get_heatmap(collection: Collection) -> list[HeatMap]:
    heatmaps = collection.find().sort("severity", -1)
    return list(heatmaps)
