import logging
from typing import Any, Literal

from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pymongo import MongoClient
from pymongo.collection import Collection, Mapping

from controller.JWTmanager import JWTmanager, JWTSettings
from models.users import Login, Signup


class Mymongo(FastAPI):
    mongodb_client: MongoClient
    collection_resident: Collection[Mapping[str, Any]]
    collection_asha: Collection[Mapping[str, Any]]
    collection_bmo: Collection[Mapping[str, Any]]
    collection_govt: Collection[Mapping[str, Any]]


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

COLLECTION_MAP = {
    "asha": app.collection_asha,
    "resident": app.collection_resident,
    "bmo": app.collection_bmo,
    "govt": app.collection_govt,
}

DB_URL = "mongodb+srv://test:test@cluster0.yvlq9mj.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
jwt_manager = JWTmanager(JWTSettings())


@app.on_event("startup")
async def startup_client():
    app.mongodb_client = MongoClient(DB_URL)
    app.collection_asha = app.mongodb_client["jalaarogya"]["asha"]
    app.collection_bmo = app.mongodb_client["jalaarogya"]["bmo"]
    app.collection_resident = app.mongodb_client["jalaarogya"]["resident"]
    app.collection_govt = app.mongodb_client["jalaarogya"]["govt"]


@app.post("/login/{role}")
async def login_endpoint(
    role: Literal["asha", "resident", "bmo", "govt"], details: Login
):
    from controller.auth import login
    from models.response import TokenPayload

    if role not in ["asha", "resident", "bmo", "govt"]:
        return {"success": False, "error": "Invalid Role"}

    user = login(details.email, details.password, COLLECTION_MAP[role], role)
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

    user = register(
        details.name,
        details.email,
        details.password,
        details.emp_id,
        COLLECTION_MAP[role],
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

    try:
        payload = jwt_manager.verify(token)
        request.state.user = payload
    except Exception as e:
        logger.error(f"Token verification failed: {e}")
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={"success": False, "error": "Invalid or expired token"},
        )
    return await call_next(request)


@app.get("/protected-route")
async def protected_route(request: Request):
    user = request.state.user
    return {
        "success": True,
        "message": f"Hello, {user}. You have accessed a protected route!",
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
