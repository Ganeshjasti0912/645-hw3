from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import date

class Survey(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    first_name: str
    last_name: str
    street: str
    city: str
    state: str
    zip: str
    phone: str
    email: str
    survey_date: date
    liked_most: Optional[str] = None
    interest_source: Optional[str] = None
    recommendation: Optional[str] = None
