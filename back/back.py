import mariadb
import os
from datetime import datetime
from fastapi import FastAPI

connection = mariadb.connect(host=os.getenv('DB_HOST'),
                             database=os.getenv('DB_NAME'),
                             user=os.getenv('DB_USER'),
                             password=os.getenv('DB_PASSWORD'))
cursor = connection.cursor(dictionary=True)

app = FastAPI()

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

@app.get('/statistics/daily/{sensor_id}/{year}/{month}/{day}')
async def get_hourly_statistics(sensor_id, year, month, day):
    queried_datetime = datetime(int(year),
                                int(month),
                                int(day))
    cursor.execute('SELECT * FROM statistic_daily WHERE sensor_id = ? AND datetime = ?',
                   (sensor_id,
                    queried_datetime.isoformat()))
    return cursor.fetchall()
