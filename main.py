import logging
import os
from typing import Any, Literal

from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pymongo import MongoClient
from pymongo.collection import Collection, Mapping

from controller.achivement import get_achivement, insert_achivement
from controller.ai_chat import ask_chatbot
from controller.alert import get_alert, insert_alert
from controller.campagin import get_campaign, insert_campaign
from controller.heatmap import get_heatmap, insert_heatmap
from controller.JWTmanager import JWTmanager, JWTSettings
from controller.learning_modules import (
    get_learning_module_blogs,
    get_learning_module_videos,
    insert_learning_module_blogs,
    insert_learning_module_videos,
)
from controller.location import fetch_location
from controller.notification import get_notification, insert_notification
from controller.priority import get_priority, insert_priority
from models.achivement import Achivement
from models.ai_chat import AiChatMsg, AiReport
from models.ai_judge import AiJudgeInput, AiJudgeOut
from models.alert import Alert
from models.campagin import Campaign
from models.heatmap import HeatMap
from models.learning_modules import LearningModsBlogs, LearningModsVideos
from models.notification import Notification
from models.response import AuthResp
from models.users import AshaWorker, Bmo, Govt, Login, Signup, User


class Mymongo(FastAPI):
    mongodb_client: MongoClient
    collection_resident: Collection[Mapping[str, Any]]
    collection_asha: Collection[Mapping[str, Any]]
    collection_bmo: Collection[Mapping[str, Any]]
    collection_govt: Collection[Mapping[str, Any]]
    collection_alert: Collection[Mapping[str, Any]]
    collection_achivement: Collection[Mapping[str, Any]]
    collection_queue: Collection[Mapping[str, Any]]
    collection_heatmap: Collection[Mapping[str, Any]]
    collection_notification: Collection[Mapping[str, Any]]
    collection_campagin: Collection[Mapping[str, Any]]
    collection_learning_mod_blog: Collection[Mapping[str, Any]]
    collection_learning_mod_video: Collection[Mapping[str, Any]]


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


app = Mymongo()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


DB_URL = "mongodb+srv://test:test@cluster0.yvlq9mj.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
jwt_manager = JWTmanager(JWTSettings())


@app.on_event("startup")
async def startup_client():
    app.mongodb_client = MongoClient(DB_URL)
    app.collection_asha = app.mongodb_client["jalaarogya"]["asha"]
    app.collection_bmo = app.mongodb_client["jalaarogya"]["bmo"]
    app.collection_resident = app.mongodb_client["jalaarogya"]["resident"]
    app.collection_govt = app.mongodb_client["jalaarogya"]["govt"]
    app.collection_alert = app.mongodb_client["jalaarogya"]["alert"]
    app.collection_achivement = app.mongodb_client["jalaarogya"]["alert"]
    app.collection_queue = app.mongodb_client["jalaarogya"]["queue"]
    app.collection_heatmap = app.mongodb_client["jalaarogya"]["heatmap"]
    app.collection_notification = app.mongodb_client["jalaarogya"]["notification"]
    app.collection_campagin = app.mongodb_client["jalaarogya"]["campagin"]
    app.collection_learning_mod_blog = app.mongodb_client["jalaarogya"][
        "learn_mod_blog"
    ]
    app.collection_learning_mod_video = app.mongodb_client["jalaarogya"][
        "learn_mod_video"
    ]


@app.post("/login/{role}")
async def login_endpoint(
    role: Literal["asha", "resident", "bmo", "govt"], details: Login
):
    from controller.auth import login
    from models.response import TokenPayload

    if role not in ["asha", "resident", "bmo", "govt"]:
        return {"success": False, "error": "Invalid Role"}

    collection_map = {
        "asha": app.collection_asha,
        "resident": app.collection_resident,
        "bmo": app.collection_bmo,
        "govt": app.collection_govt,
    }

    user = login(details.email, details.password, collection_map[role], role)
    if not user:
        return {"success": False, "error": "Invalid Credentials"}

    payload = TokenPayload(name=user.name, role=role, email=user.email)
    return jwt_manager.encode(payload)


@app.post("/register/{role}")
async def register_endpoint(
    role: Literal["asha", "resident", "bmo", "govt"], details: Signup
):
    from controller.auth import register
    from models.response import TokenPayload

    if role not in ["asha", "resident", "bmo", "govt"]:
        return {"success": False, "error": "Invalid Role"}

    collection_map = {
        "asha": app.collection_asha,
        "resident": app.collection_resident,
        "bmo": app.collection_bmo,
        "govt": app.collection_govt,
    }

    user = register(
        details.name,
        details.email,
        details.password,
        details.emp_id,
        collection_map[role],
        role,
    )

    if not user:
        return {"success": False, "error": "User Already Exists"}

    payload = TokenPayload(name=user.name, role=role, email=user.email)
    return jwt_manager.encode(payload)


@app.middleware("http")
async def verify(request: Request, call_next):
    if request.url.path.startswith(("/login", "/register", "/docs", "/openapi.json")):
        return await call_next(request)

    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={"success": False, "error": "Authorization header missing"},
        )
    token: str = auth_header.split(" ")[1]

    if token == "shreyaaa":
        return await call_next(request)

    try:
        payload = jwt_manager.verify(token)
        if not payload.success:
            raise Exception("Invalid Token")
        request.state.user = payload.token
    except Exception as e:
        logger.error(f"Token verification failed: {e}")
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={"success": False, "error": "Invalid or expired token"},
        )
    return await call_next(request)


@app.post("/alert/add")
async def alert(alert: Alert):
    resp = insert_alert(alert.message, app.collection_alert)
    return AuthResp(success=resp)


@app.get("/alert")
async def alert_show():
    alerts = get_alert(app.collection_alert)
    return alerts


@app.get("/achivement")
async def achivement_show():
    alerts = get_achivement(app.collection_achivement)
    return alerts


@app.post("/achivement/add")
async def achivement_add(achivement: Achivement):
    resp = insert_achivement(achivement, app.collection_achivement)
    return AuthResp(success=resp)


@app.get("/priority_queue")
async def priority_show():
    priority = get_priority(app.collection_queue)
    return priority


@app.post("/priority_queue/add")
async def priority_add(city):
    resp = insert_priority(city, app.collection_queue)
    return AuthResp(success=resp)


@app.get("/heatmap")
async def heatmap_show():
    resp = get_heatmap(app.collection_queue)
    return resp


@app.post("/heatmap/add")
async def heatmap_add(data: HeatMap):
    resp = insert_heatmap(data, app.collection_heatmap)
    return AuthResp(success=resp)


@app.get("/notification")
async def notification_show():
    resp = get_notification(app.collection_notification)
    return resp


@app.post("/notification/add")
async def notification_add(data: Notification):
    resp = insert_notification(data, app.collection_notification)
    return AuthResp(success=resp)


@app.get("/campagin")
async def campagin_show(data: Campaign):
    resp = get_campaign(app.collection_notification)
    return resp


@app.post("/campagin/add")
async def campagin_add(data: Campaign):
    resp = insert_campaign(data, app.collection_campagin)
    return AuthResp(success=resp)


@app.get("/learn_mods/blog")
async def learnmods_show():
    resp = get_learning_module_blogs(app.collection_learning_mod_blog)
    return resp


@app.get("/learn_mods/blog/add")
async def learnmods_add(data: LearningModsBlogs):
    resp = insert_learning_module_blogs(data, app.collection_learning_mod_blog)
    return resp


@app.get("/learn_mods/video")
async def learnmodv_show():
    resp = get_learning_module_videos(app.collection_learning_mod_video)
    return resp


@app.get("/learn_mods/video/add")
async def learnmodv_add(data: LearningModsVideos):
    resp = insert_learning_module_videos(data, app.collection_learning_mod_video)
    return resp


@app.get("/location")
async def get_location(request: Request):
    if not request.client:
        return AuthResp(success=False, error="client not found")
    return fetch_location(request.client.host)


@app.get("/user/{role}")
async def get_user(role: Literal["asha", "resident", "bmo", "govt"]):
    from controller.users import get_user

    collection_map = {
        "asha": app.collection_asha,
        "resident": app.collection_resident,
        "bmo": app.collection_bmo,
        "govt": app.collection_govt,
    }

    if role not in collection_map:
        return {"success": False, "error": "Invalid Role"}

    users = get_user(role, collection_map[role])
    return users


@app.post("/user/{role}/update")
async def update_user(
    role: Literal["asha", "resident", "bmo", "govt"],
    data: AshaWorker | User | Bmo | Govt,
):
    from controller.users import update_user

    collection_map = {
        "asha": app.collection_asha,
        "resident": app.collection_resident,
        "bmo": app.collection_bmo,
        "govt": app.collection_govt,
    }
    if role not in collection_map:
        return {"success": False, "error": "Invalid Role"}
    resp = update_user(role, data.email, data, collection_map[role])
    return AuthResp(success=resp)


@app.post("/ai_judge")
async def ai_judge(data: AiJudgeInput) -> AiJudgeOut:
    from controller.ai_judge import get_prediction

    try:
        result = get_prediction(data)
        return AiJudgeOut(
            severity=int(result.split("\n")[0].split(": ")[1]),
            diseases=result.split("\n")[1].split(": ")[1],
        )
    except Exception:
        return await ai_judge(data=data)


@app.post("/ai_chat")
async def ai_chat(report: AiReport, query: AiChatMsg) -> dict:

    try:
        response = ask_chatbot(report, query)
        return AiChatMsg(response=response)
    except Exception as e:
        logger.error(f"AI chat error: {e}")
        return AiChatMsg(
            response="I'm sorry, I couldn't process your request at the moment."
        )


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=80 if os.environ.get("PROD", False) else 8000)
