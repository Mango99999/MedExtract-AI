from typing import List, Optional

from pydantic import BaseModel, ConfigDict


class Medication(BaseModel):
    name: Optional[str] = None
    dose: Optional[str] = None
    frequency: Optional[str] = None
    duration: Optional[str] = None


class MedicalExtraction(BaseModel):
    model_config = ConfigDict(extra="forbid")

    chief_complaint: Optional[str] = None
    symptoms: List[str] = []
    diagnosis: List[str] = []
    medical_history: List[str] = []
    medications: List[Medication] = []
    procedures: List[str] = []
    follow_up: Optional[str] = None
    summary: Optional[str] = None
    risk_indicators: List[str] = []
    urgency: Optional[str] = None