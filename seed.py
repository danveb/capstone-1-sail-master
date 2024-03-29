"""Seed Database with sample data from CSV File"""

from csv import DictReader
from app import db, app 
from models import Club, db 

db.drop_all() 
db.create_all() 

with open('marinas-list.csv') as clubs:
    db.session.bulk_insert_mappings(Club, DictReader(clubs)) 
    
db.session.commit() 