from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow_sqlalchemy.fields import Nested
from models import Company

class CompanySchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Company
        include_relationships = True
        load_instance = True

    competitors = Nested('self', many=True, exclude=('competitors',))
