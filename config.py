from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, competitor_association, Company

db_path = 'postgresql+psycopg2://postgres:Nino@localhost:5432/Comp'
engine = create_engine(db_path)



try:
    
    print('Connection established')
   
    Base.metadata.create_all(bind=engine)

    Session = sessionmaker(bind=engine)
    session = Session()

    
    
except Exception as e:
    print(e)