from pydantic import BaseModel

class DevOpsQuery(BaseModel):
    query: str
    tool: str   # NEW