from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
from models import db, Company, competitor_association
from schemas import CompanySchema
from dotenv import load_dotenv
import os
from sqlalchemy import text

load_dotenv()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
ma = Marshmallow(app)
migrate = Migrate(app, db)

with app.app_context():
    db.create_all()

#Récupérer toutes les entreprises
@app.route('/companies', methods=['GET'])
def get_companies():
    companies = Company.query.all()
    company_schema = CompanySchema(many=True)
    return jsonify(company_schema.dump(companies))

#Récupérer une entreprise par son id
@app.route('/company/<int:id>', methods=['GET'])
def get_company(id):
    company = Company.query.get_or_404(id)
    company_schema = CompanySchema()
    return jsonify(company_schema.dump(company))

#Récupérer une entreprise par son nom
@app.route('/company/<string:name>', methods=['GET'])   
def get_company_by_name(name):
    company = Company.query.filter_by(name=name).first()
    if company is None:
        return jsonify({"error": "Company not found"}), 404
    company_schema = CompanySchema()
    return jsonify(company_schema.dump(company))

#Récupérer les concurrents d'une entreprise par son id
@app.route('/company/<int:id>/competitors', methods=['GET'])    
def get_company_competitors(id):
    company = Company.query.get_or_404(id)
    competitors = company.competitors
    if not competitors:
        return jsonify({"error": "Company not found"}), 404
    company_schema = CompanySchema(many=True)
    return jsonify(company_schema.dump(competitors))

#Récupérer les concurrents d'une entreprise par son nom
@app.route('/company/<string:name>/competitors', methods=['GET'])
def get_company_competitors_by_name(name):
    company = Company.query.filter_by(name=name).first()
    if company is None:
        return jsonify({"error": "Company not found"}), 404
    competitors = company.competitors
    company_schema = CompanySchema(many=True)
    return jsonify(company_schema.dump(competitors))
    
#Ajouter une entreprise
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

#Associé un concurrent à une entreprise par son id
@app.route('/company/<int:id>/competitors', methods=['POST'])   
def add_competitor(id):
    company = Company.query.get_or_404(id)
    competitor_id = request.json.get('competitor_id')
    if not competitor_id:
        return jsonify({"error": "competitor_id is required"}), 400
    competitor = Company.query.get_or_404(competitor_id)
    company.add_competitor(competitor)
    db.session.commit()
    company_schema = CompanySchema()
    return jsonify(company_schema.dump(company))

#Modifier une entreprise par son id
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

@app.route('/company/<int:id>/competitors', methods=['DELETE'])
def delete_coompetitor(id):
    company = Company.query.get_or_404(id)
    competitor_id = request.json.get('competitor_id')
    if not competitor_id:
        return jsonify({"error": "competitor_id is required"}), 400
    competitor = Company.query.get_or_404(competitor_id)
    company.competitors.remove(competitor)
    db.session.commit()
    company_schema = CompanySchema()
    return jsonify(company_schema.dump(company))
    
@app.route('/test_db_connection', methods=['GET'])
def test_db_connection():
    try:
        db.session.execute(text('SELECT 1'))
        return jsonify({"message": "Connexion réussie à la base de données"}), 200
    except Exception as e:
        return jsonify({"message": f"Erreur de connexion à la base de données : {e}"}), 500



if __name__ == '__main__':
    app.run(debug=True)

#PP8
