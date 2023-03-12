import mariadb
import os
from datetime import date
from datetime import datetime
from datetime import timedelta
from distutils.util import strtobool
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine, text


host = os.getenv('DB_HOST')
database = os.getenv('DB_NAME')
user = os.getenv('DB_USER')
password = os.getenv('DB_PASSWORD')
echo = strtobool(os.getenv('DB_ECHO', default="false"))

dsn = f"mariadb+mariadbconnector://{user}:{password}@{host}/{database}"

engine = create_engine(dsn, echo=echo)

app = FastAPI()

origins = ['*'] #TODO restrict!
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"])

@app.get('/')
async def root():
    return {'message': 'Hello world!'}

@app.get('/radars')
async def list_radars():
    with engine.connect() as conn:
        res = conn.execute(text('SELECT id, address, latitude, longitude, speed_limit FROM sensor'))
        return res.mappings().all()

@app.get('/statistics/hourly/{sensor_id}/{year}/{month}/{day}/{hour}')
async def get_hourly_statistics(sensor_id, year, month, day, hour):
    queried_datetime = datetime(int(year),
                                int(month),
                                int(day),
                                int(hour))
    with engine.connect() as conn:
        stmt = text('SELECT * '
                    'FROM statistic_hourly '
                    'WHERE sensor_id = :sensor_id '
                    'AND datetime = :queried_datetime')
        res = conn.execute(stmt,
                           {'sensor_id': sensor_id,
                            'queried_datetime': queried_datetime.isoformat()})
        return res.mappings().one()

@app.get('/statistics/hourly/{sensor_id}/{year}/{month}/{day}')
async def get_hourly_statistics(sensor_id, year, month, day):
    queried_datetime_start = datetime(int(year),
                                      int(month),
                                      int(day))
    queried_datetime_end = datetime(int(year),
                                    int(month),
                                    int(day)) + timedelta(days=1)
    with engine.connect() as conn:
        stmt = text('SELECT * '
                    'FROM statistic_hourly '
                    'WHERE sensor_id = :sensor_id '
                    'AND datetime >= :queried_datetime_start '
                    'AND datetime < :queried_datetime_end')
        res = conn.execute(stmt,
                           {'sensor_id': sensor_id,
                            'queried_datetime_start': queried_datetime_start.isoformat(),
                            'queried_datetime_end': queried_datetime_end.isoformat()})
        return res.mappings().all()

@app.get('/statistics/hourly/{sensor_id}/yesterday')
async def get_hourly_statistics_yesterday(sensor_id):
    queried_datetime_start = date.today() - timedelta(days=1)
    return await get_hourly_statistics(sensor_id,
                                       queried_datetime_start.year,
                                       queried_datetime_start.month,
                                       queried_datetime_start.day)

@app.get('/statistics/hourly/{sensor_id}/latest')
async def get_hourly_statistics_latest(sensor_id):
    with engine.connect() as conn:
        stmt = text('SELECT datetime '
                    'FROM measurement '
                    'ORDER BY datetime DESC '
                    'LIMIT 1')
        res = conn.execute(stmt)
        latest_datetime = res.mappings().one()["datetime"]

    return await get_hourly_statistics(sensor_id,
                                       latest_datetime.year,
                                       latest_datetime.month,
                                       latest_datetime.day)

@app.get('/statistics/daily/{sensor_id}/{year}/{month}/{day}')
async def get_daily_statistics(sensor_id, year, month, day):
    queried_datetime = datetime(int(year),
                                int(month),
                                int(day))
    with engine.connect() as conn:
        stmt = text('SELECT * '
                    'FROM statistic_hourly '
                    'WHERE sensor_id = :sensor_id '
                    'AND datetime = :queried_datetime')
        res = conn.execute(stmt,
                           {'sensor_id': sensor_id,
                            'queried_datetime': queried_datetime.isoformat()})
        return res.mappings().one()

@app.get('/statistics/daily/{sensor_id}/yesterday')
async def get_daily_statistics_yesterday(sensor_id):
    queried_datetime = date.today() - timedelta(days=1)
    return await get_daily_statistics(sensor_id,
                                      queried_datetime.year,
                                      queried_datetime.month,
                                      queried_datetime.day)

@app.get('/statistics/daily/{sensor_id}/latest')
async def get_daily_statistics_yesterday(sensor_id):
    with engine.connect() as conn:
        stmt = text('SELECT datetime '
                    'FROM measurement '
                    'ORDER BY datetime DESC '
                    'LIMIT 1')
        res = conn.execute(stmt)
        latest_datetime = res.mappings().one()["datetime"]
    return await get_daily_statistics(sensor_id,
                                      latest_datetime.year,
                                      latest_datetime.month,
                                      latest_datetime.day)
