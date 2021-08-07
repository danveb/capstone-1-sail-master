# sail-master

> https://sail-master.herokuapp.com/

Sail-master is an application that lets users know if sailing conditions are appropriate to enjoy a day out to sail. 

User can register for an account and able to enjoy all features of the application. 

A list of major sailing clubs is on database, which the user is able to view and choose from. 

User can create a voyage (start-point and end-point) and based on weather conditions the application provides a recommendation whether it's safe or not to sail today. 

Wind speed is the main safety measure this application reads in order to provide a recommendation to sailors. 

> Steps to run locally

1. Run virtual environment 
* `$ python3 -m venv venv`
* `$ source venv/bin/activate`

2. Install dependencies (Flask)
* `$ pip3 install -r requirements.txt`

3. Create PostgreSQL database 
* `$ createdb sail_master`

4. Run ipython and populate database with Club data (CSV format)
* `$ ipython`
* `[1] %run app.py`
* `[2] %run seed.py`

1. Run Flask 
* `$ flask run`

> API
*  `OpenweatherMap API: https://openweathermap.org/api`

> Technology
* Using Python 3.7.9 with Flask, SQLAlchemy, WTForms
* PostgreSQL for database 


### **Happy Sailing!**