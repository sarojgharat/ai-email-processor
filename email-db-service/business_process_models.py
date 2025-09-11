from sqlalchemy import Column, Integer, String, ForeignKey, JSON
from sqlalchemy.orm import relationship
from database import Base

class BusinessProcess(Base):
    """
    Represents a business process.
    """
    __tablename__ = "business_processes"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)
    description = Column(String)

    # Relationship to ClassificationCategory
    classification_categories = relationship("ClassificationCategory", back_populates="process", cascade="all, delete-orphan")

class ClassificationCategory(Base):
    """
    Represents a classification category within a business process.
    """
    __tablename__ = "classification_categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    process_id = Column(Integer, ForeignKey("business_processes.id"))

    # Relationship to BusinessProcess
    process = relationship("BusinessProcess", back_populates="classification_categories")
    # Relationship to DataExtractionFormat
    data_extraction_formats = relationship("DataExtractionFormat", back_populates="category", cascade="all, delete-orphan")

class DataExtractionFormat(Base):
    """
    Defines the data extraction format for a classification category.
    """
    __tablename__ = "data_extraction_formats"

    id = Column(Integer, primary_key=True, index=True)
    format_name = Column(String, nullable=False)
    format_definition = Column(JSON, nullable=False) # Stores the extraction schema (e.g., as JSON)
    category_id = Column(Integer, ForeignKey("classification_categories.id"))

    # Relationship to ClassificationCategory
    category = relationship("ClassificationCategory", back_populates="data_extraction_formats")
