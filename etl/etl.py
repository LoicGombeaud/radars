import argparse
import mariadb
import numpy
import os
import requests
from datetime import date
from datetime import datetime
from datetime import time
from datetime import timedelta
from dateutil import parser


# Parse input arguments
parser = argparse.ArgumentParser()
parser.add_argument('--db-host',
                    default=os.getenv('DB_HOST',
                                      default='radars-mariadb'))
parser.add_argument('--db-name',
                    default=os.getenv('DB_NAME',
                                      default='radars'))
parser.add_argument('--db-user',
                    default=os.getenv('DB_USER'))
parser.add_argument('--db-password',
                    default=os.getenv('DB_PASSWORD'))
parser.add_argument('--skip-initial-load',
                    action='store_true')
args = parser.parse_args()

# Define URL from which to retrieve measurement data
url = 'https://opendata.bordeaux-metropole.fr/api/v2/catalog/datasets/radar_pedagogique_24h/exports/csv?limit=-1&offset=0&timezone=UTC'

# Inject measurement data into the DB
connection = mariadb.connect(host=args.db_host,
                             database=args.db_name,
                             user=args.db_user,
                             password=args.db_password,
                             autocommit=True)
cursor = connection.cursor()

if args.skip_initial_load:
    print('Skipping initial load')
else:
    print('Downloading measurement data...')
    r = requests.get(url)
    with open('measurements.csv', 'w') as measurements_file:
        measurements_file.write(r.content.decode('utf-8'))
    print('Done')

    print('Loading measurement data into the DB...')
    with open('measurements.csv', 'r') as measurements_file:
        # Skip CSV header
        measurements_file.readline()
        while (line := measurements_file.readline().rstrip()):
            data = line.split(';')
            dt = data[2].split('+')[0]
            cursor.execute('INSERT IGNORE INTO measurement (id, sensor_id, datetime, speed) VALUES (?, ?, ?, ?)',
                           (data[0], data[1], dt, data[3]))
    connection.commit()

yesterday_midnight = datetime.combine(date.today() - timedelta(days=1), time.min)
cursor.execute('SELECT COUNT(*) FROM measurement WHERE datetime >= ? AND datetime < ?',
               (yesterday_midnight.isoformat(),
                (yesterday_midnight + timedelta(days=1)).isoformat()))
print('%s measurements loaded' % cursor.fetchone()[0])

# Compute statistics 

yesterday_midnight = datetime.combine(date.today() - timedelta(days=1), time.min)

cursor.execute('SELECT DISTINCT sensor_id FROM measurement WHERE datetime >= ? AND datetime < ?',
               (yesterday_midnight.isoformat(),
                (yesterday_midnight + timedelta(days=1)).isoformat()))
sensors = cursor.fetchall()

print('Computing statistics...')

for sensor in sensors:
    sensor_id = sensor[0]

    # Daily statistics
    cursor.execute('SELECT speed FROM measurement WHERE datetime >= ? AND datetime < ? AND sensor_id = ?',
                   (yesterday_midnight.isoformat(),
                    (yesterday_midnight + timedelta(days=1)).isoformat(),
                    sensor_id))
    speeds = cursor.fetchall()

    n_total = len(speeds)
    if n_total == 0:
        continue

    histo = numpy.histogram(speeds, bins=[0, 30.01, 40.01, 50.01, 60.01, 70.01, 300])[0]

    v_avg = numpy.average(speeds)
    v_50p = numpy.percentile(speeds, 50)
    v_85p = numpy.percentile(speeds, 85)
    v_max = numpy.percentile(speeds, 100)

    cursor.execute('INSERT IGNORE INTO statistic_daily VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)',
                   (sensor_id,
                    yesterday_midnight.isoformat(),
                    n_total,
                    histo[0].item(),
                    histo[1].item(),
                    histo[2].item(),
                    histo[3].item(),
                    histo[4].item(),
                    histo[5].item(),
                    v_avg,
                    v_50p,
                    v_85p,
                    v_max))

    # Hourly statistics 
    for hour in range(0, 24):
        start_datetime = yesterday_midnight + timedelta(hours=hour)
        end_datetime = yesterday_midnight + timedelta(hours=hour+1)
        cursor.execute('SELECT speed FROM measurement WHERE datetime >= ? AND datetime < ? AND sensor_id = ?',
                       (start_datetime.isoformat(),
                        end_datetime.isoformat(),
                        sensor_id))
        speeds = cursor.fetchall()

        n_total = len(speeds)
        if n_total == 0:
            continue

        histo = numpy.histogram(speeds, bins=[0, 30.01, 40.01, 50.01, 60.01, 70.01, 300])[0]

        v_avg = numpy.average(speeds)
        v_50p = numpy.percentile(speeds, 50)
        v_85p = numpy.percentile(speeds, 85)
        v_max = numpy.percentile(speeds, 100)

        cursor.execute('INSERT IGNORE INTO statistic_hourly VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)',
                       (sensor_id,
                        start_datetime,
                        n_total,
                        histo[0].item(),
                        histo[1].item(),
                        histo[2].item(),
                        histo[3].item(),
                        histo[4].item(),
                        histo[5].item(),
                        v_avg,
                        v_50p,
                        v_85p,
                        v_max))

cursor.execute('SELECT COUNT(*) FROM statistic_daily WHERE datetime >= ? AND datetime < ?',
               (yesterday_midnight.isoformat(),
                (yesterday_midnight + timedelta(days=1)).isoformat()))
print('%s daily statistics computed' % cursor.fetchone()[0])

cursor.execute('SELECT COUNT(*) FROM statistic_hourly WHERE datetime >= ? AND datetime < ?',
               (yesterday_midnight.isoformat(),
                (yesterday_midnight + timedelta(days=1)).isoformat()))
print('%s hourly statistics computed' % cursor.fetchone()[0])

cursor.close()
connection.close()
