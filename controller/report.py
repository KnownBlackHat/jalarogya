from pymongo.collection import Collection

from models.report import Report


def insert_report(data: Report, collection: Collection) -> bool:
    result = collection.insert_one(data.dict())
    return result.acknowledged


def get_reports(collection: Collection) -> list[Report]:
    reports = collection.find().sort("_id", -1)
    return [Report(**doc) for doc in list(reports)]
