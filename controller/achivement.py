from pymongo.collection import Collection

from models.achivement import Achivement


def insert_achivement(achivement: Achivement, collection: Collection) -> bool:
    achivement_dict = achivement.dict()
    result = collection.insert_one(achivement_dict)
    return result.acknowledged


def get_achivement(collection: Collection, limit: int = 10) -> list[dict]:
    achivements = collection.find().sort("_id", -1).limit(limit)
    return list(achivements)
