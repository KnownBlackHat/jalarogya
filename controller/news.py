from pymongo.collection import Collection

from models.news import News


def insert_news(data: News, collection: Collection) -> bool:
    result = collection.insert_one(data.dict())
    return result.acknowledged


def get_news(collection: Collection) -> list[News]:
    news_documents = collection.find().sort("_id", -1)
    return [News(**doc) for doc in list(news_documents)]
