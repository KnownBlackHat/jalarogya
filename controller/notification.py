from pymongo.collection import Collection

from models.notification import Notification


def insert_notification(data: Notification, collection: Collection) -> bool:
    result = collection.insert_one(data.dict())
    return result.acknowledged


def get_notification(collection: Collection) -> list[Notification]:
    notifications = collection.find()
    return [Notification(**doc) for doc in list(notifications)]
