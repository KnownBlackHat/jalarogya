from pymongo.collection import Collection

from models.news import News


def insert_news(data: News, collection: Collection) -> bool:
    result = collection.insert_one(data.dict())
    return result.acknowledged


def get_news(collection: Collection) -> list[News]:
    news_list = collection.find().sort("_id", -1)
    news_documents = list(news_list)
    news_objects = [News(**doc) for doc in news_documents]
    return news_objects
