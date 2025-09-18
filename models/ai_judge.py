from pydantic import BaseModel


class AiJudgeInput(BaseModel):
    ph: float
    turbidity: float
    electrical_conductivity: float
    chlorine: float
    bacteria_level: bool


class AiJudgeOut(BaseModel):
    severity: int
    diseases: str
