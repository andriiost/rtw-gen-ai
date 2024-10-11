from . import db, ma
from .models import Accommodation, Industry, InjuryNature, InjuryLocation, Document

class IndustrySchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Industry
        load_instance = True
        sqla_session = db.session

class InjuryNatureSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = InjuryNature
        load_instance = True
        sqla_session = db.session

class InjuryLocationSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = InjuryLocation
        load_instance = True
        sqla_session = db.session

class AccommodationSchema(ma.SQLAlchemyAutoSchema):
    # Late binding as DocumentSchema is defined later
    document = ma.Nested("DocumentSchema", exclude=('accommodations',)) # Exclusion to eliminate circular reference
    industries = ma.List(ma.Nested(IndustrySchema))
    injury_natures = ma.List(ma.Nested(InjuryNatureSchema))
    injury_locations = ma.List(ma.Nested(InjuryLocationSchema))

    class Meta:
        # Automatically maps fields
        model = Accommodation
        load_instance = True
        sqla_session = db.session

class DocumentSchema(ma.SQLAlchemyAutoSchema):
    accommodations = ma.List(ma.Nested(AccommodationSchema, exclude=('document',))) # Exclusion to eliminate circular reference

    class Meta:
        model = Document
        load_instance = True
        sqla_session = db.session
