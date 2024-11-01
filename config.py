from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import db, competitor_association, Company
from flask import Flask

# Define the Flask application instance
app = Flask(__name__)

db_path = 'postgresql+psycopg2://postgres:Nino@localhost:5432/Comp'
engine = create_engine(db_path)

try:
    print('Connection established')
    
    # Use the app context
    with app.app_context():
        db.metadata.create_all(bind=engine)

    Session = sessionmaker(bind=engine)
    session = Session()

    company = Company.query.all()
    print(company)

except Exception as e:
    print(e)