from app import ma

class DocumentSchema(ma.Schema):
    class Meta:
        fields = ('document_id', 'document_name', 'url')

class IndustrySchema(ma.Schema):
    class Meta:
        fields = ('industry_id', 'industry_name')

class InjuryNatureSchema(ma.Schema):
    class Meta:
        fields = ('injury_nature_id', 'injury_nature_name')

class InjuryLocationSchema(ma.Schema):
    class Meta:
        fields = ('injury_location_id', 'injury_location_name')

class AccommodationSchema(ma.Schema):
    document = ma.Nested(DocumentSchema)
    industries = ma.List(ma.Nested(IndustrySchema))
    injury_natures = ma.List(ma.Nested(InjuryNatureSchema))
    injury_locations = ma.List(ma.Nested(InjuryLocationSchema))

    class Meta:
        # The fields are ordered explicitly here
        fields = ('accommodation_id', 'accommodation_name', 'accommodation_description', 
                  'verified', 'date_created', 'document', 'industries', 
                  'injury_natures', 'injury_locations')
        ordered = True  # Ensures the order is respected
