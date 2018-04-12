import sqlite3 as sqlite
import csv
import json
from bs4 import BeautifulSoup
import requests
import requests.auth

from reddit_secrets import *


CLIENT_ID = client_id
CLIENT_SECRET = client_secret
PASSWORD = password
USERNAME = username



DBNAME = '507_final_reddit.db'


### implement caching ###
# CACHE_FNAME = 'reddit_cache.json'
# try:
#     cache_file_name = open(CACHE_FNAME, 'r')
#     cache_contents_string = cache_file_name.read()
#     CACHE_DICTION = json.loads(cache_contents_string)
#     cache_file.close()
# except:
#     CACHE_DICTION = {}


#### create database ###

# BARSCSV = 'flavors_of_cacao_cleaned.csv'
# COUNTRIESJSON = 'countries.json'   #### --> need to fill in what kind of data using

def create_reddit_db():
    try:
        conn = sqlite.connect(DBNAME)
        cur = conn.cursor()
    except:
        print("Could not connect to initial cursor. Try again.")

    statement = '''
        DROP TABLE IF EXISTS 'PostContent';
    ''' 
    cur.execute(statement)
    conn.commit()

    statement = '''
        DROP TABLE IF EXISTS "PostVotes";
    ''' 
    cur.execute(statement)
    conn.commit()



    create_table_one = '''
        CREATE TABLE "PostContent"(
        "ID" SERIAL PRIMARY KEY,
        "Post_Id" TEXT NOT NULL,
        "Subcategory_Name" TEXT NOT NULL,
        "Subcategory_Id" INTEGER NOT NULL,
        "Post_Date" TEXT NOT NULL,
        "Post_Time" TEXT NOT NULL,
        "Post_Title" TEXT NOT NULL,
        "Contains_photo" NUMERIC NOT NULL,
        "Contains_video" NUMERIC NOT NULL,
        "Contains_link" NUMERIC NOT NULL
        )'''

    cur.execute(create_table_one)
    conn.commit

    cur.execute('''CREATE TABLE IF NOT EXISTS PostVotes(
                "ID" SERIAL PRIMARY KEY,
                "Post_Id" TEXT NOT NULL,
                "Subcategory_Name" TEXT NOT NULL,
                "Subcategory_Id" INTEGER NOT NULL,
                "Number_Upvotes" INTEGER NOT NULL,
                "Number_Downvotes" INTEGER NOT NULL)
                ''')

    conn.commit()
    conn.close()


def populate_reddit_db():
    conn = sqlite.connect(DBNAME)
    cur = conn.cursor()
    pass


## gets saved token from cache

def get_reddit_data():
    pass




CACHE_DICTION = {}

headers = {"Authorization": "bearer fhTdafZI-0ClEzzYORfBSCR7x3M", "User-Agent": "ChangeMeClient/0.1 by YourUsername"}

client_auth = requests.auth.HTTPBasicAuth(client_id, client_secret)
post_data = {'grant_type': 'password', 'username': USERNAME, 'password': PASSWORD}
headers = {"User-Agent": "test script by /u/" + USERNAME}
response = requests.post("https://www.reddit.com/api/v1/access_token", auth=client_auth, data=post_data, headers=headers)
# cred = json.loads(response.text)


# response = requests.get("https://oauth.reddit.com/api/v1/me", headers=headers)
print(response.json())
 # {u'comment_karma': 0,
 # u'created': 1389649907.0,
 # u'created_utc': 1389649907.0,
 # u'has_mail': False,
 # u'has_mod_mail': False,
 # u'has_verified_email': None,
 # u'id': u'1',
 # u'is_gold': False,
 # u'is_mod': True,
 # u'link_karma': 1,
 # u'name': u'reddit_bot',
 # u'over_18': True}








#### NOT USING RIGHT NOW #####
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
# def setup_database():


create_reddit_db()