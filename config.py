from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, competitor_association, Company

db_path = 'postgresql+psycopg2://postgres:Nino@localhost:5432/Comp'
engine = create_engine(db_path)



try:
    
    print('Connection established')
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    Session = sessionmaker(bind=engine)
    session = Session()

    nestle = Company(id =1, name='Nestle', domain='nestle.com', location='Vevey, Switzerland', description='Food and Beverage')
    session.add(nestle)
    session.commit()

    danone = Company(id =2, name='Danone', domain='danone.com', location='Paris, France', description='Food and Beverage')
    unilever = Company(id =3, name='Unilever', domain='unilever.com', location='London, UK', description='Food and Beverage')
    
    nestle.competitors.append(danone)
    nestle.competitors.append(unilever)

    session.add(danone)

    session.commit()

    nestle = session.query(Company).filter(Company.id==1).one()
    
    for competitor in nestle.competitors:
        if competitor.id ==2:

            print(competitor.name)
    
except Exception as e:
    print(e)