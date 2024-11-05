from marshmallow_sqlalchemy import SQLAlchemyAutoSchema, fields
from models import Company

class CompanySchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Company
        load_instance = True

    competitors = fields.Nested('self', many=True, exclude=('competitors',))
