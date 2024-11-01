from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
from models import db, Company, competitor_association
from schemas import CompanySchema

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://postgres:Nino@localhost:5432/Comp'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
ma = Marshmallow(app)
migrate = Migrate(app, db)

with app.app_context():
    db.create_all()

@app.route('/companies', methods=['GET'])
def get_companies():
    companies = Company.query.all()
    company_schema = CompanySchema(many=True)
    return jsonify(company_schema.dump(companies))

@app.route('/company/<int:id>', methods=['GET'])
def get_company(id):
    company = Company.query.get_or_404(id)
    company_schema = CompanySchema()
    return jsonify(company_schema.dump(company))


@app.route('/company/<int:id>/competitors', methods=['GET'])    
def get_competitors(id):
    competitors_id = competitor_association.query.filter_by(company_id=id).all()
    competitors = [Company.query.get(competitor.competitor_id) for competitor in competitors_id]
    company_schema = CompanySchema(many=True)
    return jsonify(company_schema.dump(competitors))
    

@app.route('/company', methods=['POST'])
def add_company():
    new_company = Company(
        name=request.json['name'],
        domain=request.json['domain'],
        location=request.json['location'],
        description=request.json['description']
    )
    db.session.add(new_company)
    db.session.commit()
    company_schema = CompanySchema()
    return jsonify(company_schema.dump(new_company)), 201

@app.route('/company/<int:id>/competitors', methods=['POST'])   
def add_competitor(id):
    company = Company.query.get_or_404(id)
    competitor = Company.query.get_or_404(request.json['competitor_id'])
    company.competitors.append(competitor)
    db.session.commit()
    company_schema = CompanySchema()
    return jsonify(company_schema.dump(company))

@app.route('/company/<int:id>', methods=['PUT'])
def update_company(id):
    company = Company.query.get_or_404(id)
    company.name = request.json['name']
    company.domain = request.json['domain']
    company.location = request.json['location']
    company.description = request.json['description']
    db.session.commit()
    company_schema = CompanySchema()
    return jsonify(company_schema.dump(company))

@app.route('/company/<int:id>', methods=['DELETE'])
def delete_company(id):
    company = Company.query.get_or_404(id)
    db.session.delete(company)
    db.session.commit()
    return '', 204

if __name__ == '__main__':
    app.run(debug=True)
