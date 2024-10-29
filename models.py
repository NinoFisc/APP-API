# models.py
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# Table d'association pour la relation many-to-many
competitor_association = db.Table(
    'competitor_association',
    db.Column('company_id', db.Integer, db.ForeignKey('company.id'), primary_key=True),
    db.Column('competitor_id', db.Integer, db.ForeignKey('company.id'), primary_key=True)
)

class Company(db.Model):
    __tablename__ = 'company'
    id = db.Column(db.Integer, primary_key=True, index=True)
    name = db.Column(db.String, index=True)
    domain = db.Column(db.String, index=True, unique=True)
    location = db.Column(db.String, index=True)
    description = db.Column(db.String, index=True)

    competitors = db.relationship(
        'Company',
        secondary=competitor_association,
        primaryjoin=id == competitor_association.c.company_id,
        secondaryjoin=id == competitor_association.c.competitor_id,
        backref='competitor_of'
    )

nestle = Company(id =1, name='Nestle', domain='nestle.com', location='Vevey, Switzerland', description='Food and Beverage')


