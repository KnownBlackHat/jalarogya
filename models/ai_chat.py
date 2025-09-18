from pydantic import BaseModel


class AiChatMsg(BaseModel):
    msg: str


class AiReport(BaseModel):
    hemoglobin: float
    wbc: float
    platelet_count: float
    blood_urea: float
    serum_creatinine: float
    electrolytes: float
    bilirubin: float
    sgpt_alt: float
    sgot_ast: float
