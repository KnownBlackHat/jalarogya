from pymongo.collection import Collection


def insert_priority(city: str, collection: Collection):
    result = collection.find_one_and_update(
        {"city": city}, {"$inc": {"count": 1}}, upsert=True
    )
    return result.acknowledged


def get_priority(collection: Collection) -> list[dict]:
    priorities = collection.find().sort("count", -1)
    return list(priorities)
