#!/usr/bin/env python3
import os
import glob
from playhouse.csv_loader import *
from peewee import *
import logging

database = SqliteDatabase('stm.db')
LOG_FILENAME = 'stm.log'


class BaseModel(Model):
    class Meta:
        database = database


class Agency(BaseModel):
    agency_id = CharField(primary_key=True)
    agency_name = CharField()
    agency_url = CharField()
    agency_timezone = CharField()
    agency_lang = CharField()
    agency_phone = CharField(null=True)
    agency_fare_url = CharField()


class Routes(BaseModel):
    route_id = IntegerField()
    agency_id = IntegerField()
    route_short_name = CharField()
    route_long_name = CharField()
    route_type = CharField()
    route_url = CharField()
    route_color = CharField()
    route_text_color = CharField()


class Trips(BaseModel):
    route_id = IntegerField()
    service_id = IntegerField()
    trip_id = CharField(primary_key=True)
    trip_headsign = CharField()
    direction_id = BooleanField()
    wheelchair_accessible = IntegerField()
    shape_id = IntegerField()
    note_fr = CharField(null=True)
    note_en = CharField(null=True)


class Stop_Times(BaseModel):
    trip_id = CharField()
    arrival_time = CharField()
    departure_time = CharField()
    stop_id = IntegerField()
    stop_sequence = IntegerField()


class Stops(BaseModel):
    stop_id = IntegerField(primary_key=True)
    stop_code = IntegerField()
    stop_name = CharField()
    stop_lat = IntegerField()
    stop_lon = IntegerField()
    stop_url = CharField()
    wheelchair_boarding = BooleanField()


class Calendar_Dates(BaseModel):
    service_id = IntegerField(primary_key=True)
    date = DateField()
    exception_type = BooleanField()


def create_tables():
    database.connect()
    database.create_tables([Agency, Stops,
                            Routes, Trips, Stop_Times, Calendar_Dates])

logging.basicConfig(filename=LOG_FILENAME)
logger = logging.getLogger('peewee')
logger.setLevel(logging.DEBUG)
logger.addHandler(logging.StreamHandler())


def load_data():
    stm_file_dir = os.listdir('stm/')
    for file in stm_file_dir:
        print('Loading ' + file)
        if file.endswith('.txt'):
            print(file)
            table_name = os.path.splitext(file)[0]
            print(table_name)
            file_path = "stm/" + file
            data = load_csv(database, file_path, has_header=True,
                            db_table=table_name)
