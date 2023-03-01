import mariadb
import os
from datetime import date
from datetime import datetime
from datetime import timedelta
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


pool = mariadb.ConnectionPool(host=os.getenv('DB_HOST'),
                              database=os.getenv('DB_NAME'),
                              user=os.getenv('DB_USER'),
                              password=os.getenv('DB_PASSWORD'),
                              pool_name='back',
                              pool_size=20)

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
    pconn = pool.get_connection()
    cursor = pconn.cursor(dictionary=True)
    cursor.execute('SELECT id, address, latitude, longitude, speed_limit FROM sensor')
    res = cursor.fetchall()
    cursor.close()
    pconn.close()
    return res

@app.get('/statistics/hourly/{sensor_id}/{year}/{month}/{day}/{hour}')
async def get_hourly_statistics(sensor_id, year, month, day, hour):
    queried_datetime = datetime(int(year),
                                int(month),
                                int(day),
                                int(hour))
    pconn = pool.get_connection()
    cursor = pconn.cursor(dictionary=True)
    cursor.execute('SELECT * FROM statistic_hourly WHERE sensor_id = ? AND datetime = ?',
                   (sensor_id,
                    queried_datetime.isoformat()))
    res = cursor.fetchone()
    cursor.close()
    pconn.close()
    return res

@app.get('/statistics/hourly/{sensor_id}/{year}/{month}/{day}')
async def get_hourly_statistics(sensor_id, year, month, day):
    queried_datetime_start = datetime(int(year),
                                      int(month),
                                      int(day))
    queried_datetime_end = datetime(int(year),
                                    int(month),
                                    int(day)) + timedelta(days=1)

    pconn = pool.get_connection()
    cursor = pconn.cursor(dictionary=True)
    cursor.execute('SELECT * FROM statistic_hourly WHERE sensor_id = ? AND datetime >= ? AND datetime < ?',
                   (sensor_id,
                    queried_datetime_start.isoformat(),
                    queried_datetime_end.isoformat()))
    res = cursor.fetchall()
    cursor.close()
    pconn.close()
    return res

@app.get('/statistics/hourly/{sensor_id}/yesterday')
async def get_hourly_statistics_yesterday(sensor_id):
    queried_datetime_start = date.today() - timedelta(days=1)
    return await get_hourly_statistics(sensor_id,
                                       queried_datetime_start.year,
                                       queried_datetime_start.month,
                                       queried_datetime_start.day)

@app.get('/statistics/hourly/{sensor_id}/latest')
async def get_hourly_statistics_latest(sensor_id):
    pconn = pool.get_connection()
    cursor = pconn.cursor(dictionary=True)
    cursor.execute('SELECT datetime FROM measurement ORDER BY datetime DESC LIMIT 1')
    latest_datetime = cursor.fetchone()["datetime"]
    cursor.close()
    pconn.close()
    return await get_hourly_statistics(sensor_id,
                                       latest_datetime.year,
                                       latest_datetime.month,
                                       latest_datetime.day)

@app.get('/statistics/daily/{sensor_id}/{year}/{month}/{day}')
async def get_daily_statistics(sensor_id, year, month, day):
    queried_datetime = datetime(int(year),
                                int(month),
                                int(day))
    pconn = pool.get_connection()
    cursor = pconn.cursor(dictionary=True)
    cursor.execute('SELECT * FROM statistic_daily WHERE sensor_id = ? AND datetime = ?',
                   (sensor_id,
                    queried_datetime.isoformat()))
    res = cursor.fetchone()
    cursor.close()
    pconn.close()
    return res

@app.get('/statistics/daily/{sensor_id}/yesterday')
async def get_daily_statistics_yesterday(sensor_id):
    queried_datetime = date.today() - timedelta(days=1)
    return await get_daily_statistics(sensor_id,
                                      queried_datetime.year,
                                      queried_datetime.month,
                                      queried_datetime.day)

@app.get('/statistics/daily/{sensor_id}/latest')
async def get_daily_statistics_yesterday(sensor_id):
    pconn = pool.get_connection()
    cursor = pconn.cursor(dictionary=True)
    cursor.execute('SELECT datetime FROM measurement ORDER BY datetime DESC LIMIT 1')
    latest_datetime = cursor.fetchone()["datetime"]
    cursor.close()
    pconn.close()
    return await get_daily_statistics(sensor_id,
                                      latest_datetime.year,
                                      latest_datetime.month,
                                      latest_datetime.day)
