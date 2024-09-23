from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, Date, Table, Text
from sqlalchemy.orm import relationship
from app import db

# Junction tables for many-to-many relationships
accommodation_industry = Table(
    'accommodation_industry', db.metadata,
    Column('accommodation_id', Integer, ForeignKey('accommodations.accommodation_id'), primary_key=True),
    Column('industry_id', Integer, ForeignKey('industries.industry_id'), primary_key=True)
)

accommodation_injury_nature = Table(
    'accommodation_injury_nature', db.metadata,
    Column('accommodation_id', Integer, ForeignKey('accommodations.accommodation_id'), primary_key=True),
    Column('injury_nature_id', Integer, ForeignKey('injury_natures.injury_nature_id'), primary_key=True)
)

accommodation_injury_location = Table(
    'accommodation_injury_location', db.metadata,
    Column('accommodation_id', Integer, ForeignKey('accommodations.accommodation_id'), primary_key=True),
    Column('injury_location_id', Integer, ForeignKey('injury_locations.injury_location_id'), primary_key=True)
)

class Industry(db.Model):
    __tablename__ = 'industries'
    industry_id = Column(Integer, primary_key=True, autoincrement=True)
    industry_name = Column(String, nullable=False)
    accommodations = relationship("Accommodation", secondary=accommodation_industry, back_populates="industries")

class InjuryNature(db.Model):
    __tablename__ = 'injury_natures'
    injury_nature_id = Column(Integer, primary_key=True, autoincrement=True)
    injury_nature_name = Column(String, nullable=False)
    accommodations = relationship("Accommodation", secondary=accommodation_injury_nature, back_populates="injury_natures")

class InjuryLocation(db.Model):
    __tablename__ = 'injury_locations'
    injury_location_id = Column(Integer, primary_key=True, autoincrement=True)
    injury_location_name = Column(String, nullable=False)
    accommodations = relationship("Accommodation", secondary=accommodation_injury_location, back_populates="injury_locations")

class Accommodation(db.Model):
    __tablename__ = 'accommodations'
    accommodation_id = Column(Integer, primary_key=True, autoincrement=True)
    accommodation_name = Column(String, nullable=False)
    accommodation_description = Column(Text)
    verified = Column(Boolean, default=False)
    date_created = Column(Date)
    document_id = Column(Integer, ForeignKey('documents.document_id'))
    document = relationship("Document", back_populates="accommodations")
    industries = relationship("Industry", secondary=accommodation_industry, back_populates="accommodations")
    injury_natures = relationship("InjuryNature", secondary=accommodation_injury_nature, back_populates="accommodations")
    injury_locations = relationship("InjuryLocation", secondary=accommodation_injury_location, back_populates="accommodations")

class Document(db.Model):
    __tablename__ = 'documents'
    document_id = Column(Integer, primary_key=True, autoincrement=True)
    document_name = Column(String, nullable=False)
    document_description = Column(Text)
    url = Column(String)
    extension = Column(String(10))
    text = Column(Text)
    accommodations = relationship("Accommodation", back_populates="document")
