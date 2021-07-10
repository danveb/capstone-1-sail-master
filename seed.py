"""Seed Database with sample data from CSV File"""

from csv import DictReader
from app import db 
from models import Club 

db.drop_all() 
db.create_all() 

with open('generator/marinas-list.csv') as clubs:
    db.session.bulk_insert_mappings(Club, DictReader(clubs)) 

db.session.commit() 