from pymongo.collection import Collection

from models.priority import Priority


def insert_priority(city: str, collection: Collection):
    collection.find_one_and_update({"city": city}, {"$inc": {"count": 1}}, upsert=True)
    return True


def get_priority(collection: Collection) -> list[Priority]:
    priorities = collection.find().sort("count", -1)
    return [Priority(**doc) for doc in list(priorities)]
