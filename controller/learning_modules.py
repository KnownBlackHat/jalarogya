from typing import List

from pymongo.collection import Collection

from models.learning_modules import LearningModsBlogs, LearningModsVideos


def insert_learning_module_blogs(
    data: LearningModsBlogs, collection: Collection
) -> bool:
    result = collection.insert_one(data.dict())
    return result.acknowledged


def get_learning_module_blogs(collection: Collection) -> List[LearningModsBlogs]:
    blogs = collection.find()
    return list(blogs)


def insert_learning_module_videos(
    data: LearningModsVideos, collection: Collection
) -> bool:
    result = collection.insert_one(data.dict())
    return result.acknowledged


def get_learning_module_videos(collection: Collection) -> List[LearningModsVideos]:
    videos = collection.find()
    return list(videos)
