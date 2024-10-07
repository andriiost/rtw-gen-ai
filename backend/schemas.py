from . import db, ma
from .models import Accommodation, Industry, InjuryNature, InjuryLocation, Document

class DocumentSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Document
        load_instance = True
        sqla_session = db.session

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
    document = ma.Nested(DocumentSchema)
    industries = ma.List(ma.Nested(IndustrySchema))
    injury_natures = ma.List(ma.Nested(InjuryNatureSchema))
    injury_locations = ma.List(ma.Nested(InjuryLocationSchema))

    class Meta:
        # Automatically maps fields
        model = Accommodation
        load_instance = True
        sqla_session = db.session
