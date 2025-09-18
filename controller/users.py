from typing import List, Literal

from pymongo.collection import Collection

from models.users import AshaWorker, Bmo, Govt, User


def get_user(
    role: Literal["asha", "resident", "bmo", "govt"], collection: Collection
) -> List[User | AshaWorker | Bmo | Govt]:
    match role:
        case "asha":
            bmos = collection.find()
            return [AshaWorker(**asha) for asha in bmos]
        case "resident":
            resident = collection.find()
            return [User(**usr) for usr in resident]
        case "bmo":
            bmos = collection.find()
            return [Bmo(**bmo) for bmo in bmos]
        case "govt":
            govts = collection.find()
            return [Govt(**govt) for govt in govts]


def update_user(
    role: Literal["asha", "resident", "bmo", "govt"],
    email: str,
    update_data: AshaWorker | User | Bmo | Govt,
    collection: Collection,
) -> bool:
    if role not in ["asha", "resident", "bmo", "govt"]:
        return False

    result = collection.find_one_and_update(
        {"email": email},
        {"$set": update_data.dict(exclude_unset=True)},
    )
    return result.acknowledged if result else False
