from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.sql import func

from database import Base


class Report(Base):
    __tablename__ = "reports"

    id = Column(Integer, primary_key=True, index=True)

    patient_name = Column(String(100), nullable=True)

    document_type = Column(String(50))

    ocr_text = Column(Text)

    analysis = Column(Text)

    created_at = Column(DateTime(timezone=True), server_default=func.now())