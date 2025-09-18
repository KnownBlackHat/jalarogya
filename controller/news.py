from models.news import News


def insert_news(data: News, collection) -> bool:
    result = collection.insert_one(data.dict())
    return result.acknowledged


def get_news(collection) -> list[News]:
    news_list = collection.find().sort("_id", -1)
    return list(news_list)
