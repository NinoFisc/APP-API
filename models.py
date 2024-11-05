# models.py
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# Table d'association pour la relation many-to-many symétrique
competitor_association = db.Table(
    'competitor_association',
    db.Column('company_id', db.Integer, db.ForeignKey('company.id')),
    db.Column('competitor_id', db.Integer, db.ForeignKey('company.id'))
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
        backref=db.backref('competitors_back', lazy='dynamic'),
        lazy='dynamic'
    )

    def add_competitor(self, competitor):
        if not self.is_competitor(competitor):
            self.competitors.append(competitor)
            competitor.competitors.append(self)

    def is_competitor(self, competitor):
        return self.competitors.filter(
            competitor_association.c.competitor_id == competitor.id
        ).count() > 0


