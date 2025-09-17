from pydantic import BaseModel


class LearningModsBlogs(BaseModel):
    title: str
    content: str
    conclusion: str
    user_name: str


class LearningModsVideos(BaseModel):
    title: str
    video_url: str
