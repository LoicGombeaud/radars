import mariadb
import os
from datetime import date
from datetime import datetime
from datetime import timedelta
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


connection = mariadb.connect(host=os.getenv('DB_HOST'),
                             database=os.getenv('DB_NAME'),
                             user=os.getenv('DB_USER'),
                             password=os.getenv('DB_PASSWORD'))
connection.auto_reconnect = True
cursor = connection.cursor(dictionary=True)

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
    cursor.execute('SELECT id, address, latitude, longitude, speed_limit FROM sensor')
    return cursor.fetchall()

@app.get('/statistics/hourly/{sensor_id}/{year}/{month}/{day}/{hour}')
async def get_hourly_statistics(sensor_id, year, month, day, hour):
    queried_datetime = datetime(int(year),
                                int(month),
                                int(day),
                                int(hour))
    cursor.execute('SELECT * FROM statistic_hourly WHERE sensor_id = ? AND datetime = ?',
                   (sensor_id,
                    queried_datetime.isoformat()))
    return cursor.fetchone()

@app.get('/statistics/hourly/{sensor_id}/{year}/{month}/{day}')
async def get_hourly_statistics(sensor_id, year, month, day):
    queried_datetime_start = datetime(int(year),
                                      int(month),
                                      int(day))
    queried_datetime_end = datetime(int(year),
                                    int(month),
                                    int(day)+1)
    cursor.execute('SELECT * FROM statistic_hourly WHERE sensor_id = ? AND datetime >= ? AND datetime < ?',
                   (sensor_id,
                    queried_datetime_start.isoformat(),
                    queried_datetime_end.isoformat()))
    return cursor.fetchall()

@app.get('/statistics/hourly/{sensor_id}/yesterday')
async def get_hourly_statistics(sensor_id):
    queried_datetime_start = date.today() - timedelta(days=1)
    queried_datetime_end = date.today()
    cursor.execute('SELECT * FROM statistic_hourly WHERE sensor_id = ? AND datetime >= ? AND datetime < ?',
                   (sensor_id,
                    queried_datetime_start.isoformat(),
                    queried_datetime_end.isoformat()))
    return cursor.fetchall()

@app.get('/statistics/daily/{sensor_id}/{year}/{month}/{day}')
async def get_hourly_statistics(sensor_id, year, month, day):
    queried_datetime = datetime(int(year),
                                int(month),
                                int(day))
    cursor.execute('SELECT * FROM statistic_daily WHERE sensor_id = ? AND datetime = ?',
                   (sensor_id,
                    queried_datetime.isoformat()))
    return cursor.fetchone()

@app.get('/statistics/daily/{sensor_id}/yesterday')
async def get_hourly_statistics(sensor_id):
    queried_datetime = date.today() - timedelta(days=1)
    cursor.execute('SELECT * FROM statistic_daily WHERE sensor_id = ? AND datetime = ?',
                   (sensor_id,
                    queried_datetime.isoformat()))
    return cursor.fetchone()
