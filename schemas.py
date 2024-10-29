from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from models import Company

class CompanySchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Company
        include_relationships = True
        load_instance = True