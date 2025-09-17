from pymongo.collection import Collection

from models.campaign import Campaign


def insert_campaign(data: Campaign, collection: Collection) -> bool:
    result = collection.insert_one(data.dict())
    return result.acknowledged


def get_campaign(collection: Collection) -> list[Campaign]:
    campaigns = collection.find()
    return list(campaigns)
