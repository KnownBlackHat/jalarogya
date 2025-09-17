from typing import Literal

from pymongo.collection import Collection


def login(
    email: str,
    password: str,
    collection: Collection,
    role: Literal["asha", "resident", "bmo"],
):
    if usr := collection.find_one({"email": email, "password": password}):
        match role:
            case "asha":
                from models.users import AshaWorker

                return AshaWorker(
                    emp_id=usr.get("emp_id", 0),
                    name=usr.get("name", ""),
                    email=usr.get("email", ""),
                    password=usr.get("password", ""),
                )
            case "bmo":
                from models.users import Bmo as User
            case "resident":
                from models.users import User

        return User(
            name=usr.get("name", ""),
            email=usr.get("email", ""),
            password=usr.get("password", ""),
        )
    return False


def register(
    name: str,
    email: str,
    password: str,
    collection: Collection,
    role: Literal["asha", "resident", "bmo"],
):
    if usr := collection.find_one({"email": email}):
        return False

    match role:
        case "asha":
            from models.users import AshaWorker

            emp_id = collection.count_documents({}) + 1
            user = AshaWorker(
                emp_id=emp_id,
                name=name,
                email=email,
                password=password,
            )
            collection.insert_one(user.dict())
            return user
        case "bmo":
            from models.users import Bmo as User
        case "resident":
            from models.users import User

    user = User(
        name=name,
        email=email,
        password=password,
    )
    collection.insert_one(user.dict())
    return user
