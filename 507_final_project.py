import sqlite3 as sqlite
import csv
import json
from bs4 import BeautifulSoup
import requests
import requests.auth

from reddit_secrets import *


#### scrape data ####



CACHE_FNAME = 'reddit_cache.json'
try:
    cache_file_name = open(CACHE_FNAME, 'r')
    cache_contents_string = cache_file_name.read()
    CACHE_DICTION = json.loads(cache_contents_string)
    cache_file.close()
except:
    CACHE_DICTION = {}


#### create database ###

DBNAME = '507_final_reddit.db'
# BARSCSV = 'flavors_of_cacao_cleaned.csv'
# COUNTRIESJSON = 'countries.json'   #### --> need to fill in what kind of data using

def create_choc_db():
    try:
        conn = sqlite3.connect(DBNAME)
        cur = conn.cursor()
    except:
        print("Could not connect to initial cursor. Try again.")

    ##### Drop tables if extant #####

    # statement = '''
    #     DROP TABLE IF EXISTS 'Bars';
    # ''' 
    # cur.execute(statement)
    # conn.commit()

    # statement = '''
    #     DROP TABLE IF EXISTS "Countries";
    # ''' 
    # cur.execute(statement)
    # conn.commit()

CLIENT_ID = client_id
CLIENT_SECRET = client_secret
PASSWORD = password
USERNAME = username

REDIRECT_URI = 'https://www.programsinformationpeople.org/runestone/oauth'
AUTHORIZATION_URL = 'https://ssl.reddit.com/api/v1/authorize'
TOKEN_URL = 'https://www.reddit.com/api/v1/access_token'

CACHE_DICTION = {}

##### Setting up the database connection #####
# try:
#     if db_password != "":
#         conn = psycopg2.connect("dbname = '{0}' user = '{1}' password = '{2}'".format(db_name, db_user, db_password))
#         print("Success connecting to the database")
#     else:
#         conn = psycopg2.connect("dbname = '{0}' user = '{1}'".format(db_name, db_user))
#         print("Success connecting to the database")

# except:
#     print("Unable to connect to the database")
#     sys.exit(1)

# cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

##### Seting up the database #####
def setup_database():

    cur.execute("""CREATE TABLE IF NOT EXISTS PostContent(
        		ID SERIAL PRIMARY KEY,
        		Post_Id TEXT NOT NULL
        		Subcategory_Name TEXT NOT NULL,
        		Subcategory_Id INTEGER NOT NULL,
        		Post_Date TEXT NOT NULL,
        		Post_Time TEXT NOT NULL,
        		Post_Title TEXT NOT NULL,
        		Contains_photo NUMERIC NOT NULL,
        		Contains_video NUMERIC NOT NULL,
        		Contains_link NUMERIC NOT NULL,
                """)

    cur.execute("""CREATE TABLE IF NOT EXISTS PostVotes(
                ID SERIAL PRIMARY KEY,
                Post_Id TEXT NOT NULL
        		Subcategory_Name TEXT NOT NULL,
        		Subcategory_Id INTEGER NOT NULL,
        		Number_Upvotes INTEGER NOT NULL,
        		Number_Downvotes INTEGER NOT NULL
        		""")

    conn.commit()


