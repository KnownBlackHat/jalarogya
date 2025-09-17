from typing import Literal, Optional

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
                from models.users import Bmo

                return Bmo(
                    emp_id=usr.get("emp_id", 0),
                    name=usr.get("name", ""),
                    email=usr.get("email", ""),
                    password=usr.get("password", ""),
                )
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
    emp_id: Optional[int],
    collection: Collection,
    role: Literal["asha", "resident", "bmo"],
):
    if collection.find_one({"email": email}):
        return False

    match role:
        case "asha":
            from models.users import AshaWorker

            user = AshaWorker(
                emp_id=emp_id or 0,
                name=name,
                email=email,
                password=password,
            )
            collection.insert_one(user.dict())
            return user
        case "bmo":
            from models.users import Bmo

            user = Bmo(emp_id=emp_id or 0, name=name, email=email, password=password)
        case "resident":
            from models.users import User

            user = User(
                name=name,
                email=email,
                password=password,
            )

    collection.insert_one(user.dict())
    return user
