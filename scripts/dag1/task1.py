import datetime
import requests
from sqlalchemy import Column, Integer, VARCHAR, Date, Float, TIMESTAMP
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base


Base = declarative_base()


def get_wether(city, days):
    wth_full_info = []
    URL = f'http://api.weatherapi.com/v1/forecast.json?key={KEYWETHER}&q={city}&days={days}&aqi=no&alerts=yes'
    r = requests.get(url=URL)

    resul = r.json()

    for i in range(days):
        wth_info = {
            'location': resul.get('location').get('name'),
            'date': resul.get('forecast').get('forecastday')[i].get('date'),
            'min_temp': resul.get('forecast').get('forecastday')[i].get('day').get('maxtemp_c'),
            'max_temp': resul.get('forecast').get('forecastday')[i].get('day').get('mintemp_c'),
            'avg_temp': resul.get('forecast').get('forecastday')[i].get('day').get('avgtemp_c'),
        }

        wth_full_info.append(wth_info)

    return wth_full_info

class Currency(Base):
    __tablename__='wether'
    id = Column(Integer, nullable=False, unique=True, primary_key=True, autoincrement=True)
    location = Column(VARCHAR(50), nullable=False)
    date = Column(Date, nullable=False)
    min_temp_day = Column(Float, nullable=False)
    max_temp_day = Column(Float, nullable=False)
    avg_temp_day = Column(Float, nullable=False)
    date_created = Column(TIMESTAMP, nullable=False, index=True)

engine = create_engine(SQLALCHEMY_DATABASE_URI)

Base.metadata.create_all(bind=engine)

sessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)()
session_local = sessionLocal

l_dict = get_wether('Lipetsk', 3)

for day in l_dict:
    new_wether = Currency(
        location = day['location'],
        date = day['date'],
        min_temp_day = day['min_temp'],
        max_temp_day = day['max_temp'],
        avg_temp_day = day['avg_temp'],
        date_created = datetime.datetime.now(datetime.UTC)
    )
    session_local.add(new_wether)

session_local.commit()