from __future__ import annotations

from sqlalchemy import String, Text, ForeignKey, JSON
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from pgvector.sqlalchemy import Vector

from app.models.base import Base, UUIDMixin, TimestampMixin
import uuid

class DatasetFile(Base, UUIDMixin, TimestampMixin):
    __tablename__ = 'dataset_files'

    filename: Mapped[str] = mapped_column(String(255))
    description: Mapped[str | None] = mapped_column(Text)
    category: Mapped[str | None] = mapped_column(String(255))
    metadata_json: Mapped[dict | None] = mapped_column(JSONB)
    
    chunks: Mapped[list[DatasetChunk]] = relationship(back_populates="file", cascade="all, delete-orphan")

class DatasetChunk(Base, UUIDMixin):
    __tablename__ = 'dataset_chunks'

    file_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey('dataset_files.id', ondelete='CASCADE'))
    content: Mapped[str] = mapped_column(Text)
    embedding: Mapped[list[float] | None] = mapped_column(Vector(1536))
    metadata_json: Mapped[dict | None] = mapped_column(JSONB)

    file: Mapped[DatasetFile] = relationship(back_populates="chunks")
