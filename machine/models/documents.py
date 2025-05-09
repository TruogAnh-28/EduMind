from uuid import uuid4
from core.db import Base
from datetime import datetime
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Column, String, ForeignKey, Text, DateTime, func, Integer



class Documents(Base):
    __tablename__ = "documents"
    id = Column(UUID, primary_key=True, default=uuid4)
    lesson_id = Column(UUID, ForeignKey("lessons.id", ondelete="CASCADE"), nullable=False)
    name = Column(String, nullable=False)
    type = Column(String, nullable=False)
    description = Column(String, nullable=False)
    document_url = Column(Text, nullable=False)
    status = Column(String, default="processing", nullable=False)  # "processing", "completed", "failed"
    created_at = Column(DateTime, default=func.now(), nullable=False)
    progress_upload = Column(Integer, default="0", nullable=False)

    extracted_text = relationship("ExtractedText", back_populates="document")  # changed here
    lesson = relationship("Lessons", back_populates="documents")
