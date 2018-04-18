import sqlite3 as sqlite
import csv
import json
from bs4 import BeautifulSoup
import requests
import requests.auth
from datetime import *
from reddit_secrets import *
import os


CLIENT_ID = client_id
CLIENT_SECRET = client_secret
PASSWORD = password
USERNAME = username

DBNAME = '507_final_reddit_2.db'
CACHE_FNAME = 'reddit_cache.json'


#### create database ###
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

    create_table_one = '''
        CREATE TABLE "PostContent"(
        "ID" INTEGER PRIMARY KEY AUTOINCREMENT,
        "Subreddit_Id" TEXT,
        "Subreddit_Name" TEXT,
        "Post_Id" TEXT NOT NULL,
        "subreddit_subscribers" TEXT,
        "Thread_Title" TEXT,
        "Pinned_content" TEXT,
        "Original_Content" TEXT,
        "Contains_video" TEXT
        "Number_Upvotes" INTEGER NOT NULL,
        )'''
        # "Post_Title" TEXT,        
        # "Post_Date" TEXT,
        # "Contains_link" NUMERIC NOT NULL
    cur.execute(create_table_one)
    conn.commit

    statement = '''
        DROP TABLE IF EXISTS "PostVotes";
    ''' 
    cur.execute(statement)
    conn.commit()
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


def check_cache_time():
    global CACHE_FNAME
    try:   ## if there has been a cache file already created 
        time = os.path.getctime(CACHE_FNAME)
        created_time = datetime.fromtimestamp(time)    ### i don't think this is working, i think this keeps re-setting
        print("created_time")
        print(created_time)
        current_time = datetime.now()
        print("current_time")
        print(current_time)

        change_time = current_time - created_time
        print("change_time")
        print(change_time)
        # change_time_days = change_time.days
        # print("change_time days")
        # print(change_time)
        change_time_minutes = change_time.minute
        print("change")
        print(change_time_minutes)

        print("===========change_time")
        print(change_time)

        if change_time <= 1:
            return False   ## no need to get new contents, cache is up to date
        else:
            return True  ## time to replace cache contents. 
    except:  ## means there has not been a cachefile created yet
        return False    #### --> possibly another problem to deal with later  ## THIS DOES NOT WORK!! IGNORE IT!!!


def load_cache():
    global CACHE_FNAME
    check_cache = check_cache_time()
    if check_cache is False:
        with open(CACHE_FNAME, "r") as cache_file:
            cache_string = cache_file.read()
            CACHE_DICTION = json.loads(cache_string)
        return CACHE_DICTION



#  Saves cache contents into a json file
def write_cache_data(data_to_cache):
    # full_text = json.dumps(CACHE_DICTION)
    cache_file = open(CACHE_FNAME,"w")
    cache_string = json.dumps(data_to_cache)
    cache_file.write(cache_string)
    cache_file.close()

def get_reddit_creds():
    headers = {"Authorization": "bearer fhTdafZI-0ClEzzYORfBSCR7x3M", "User-Agent": "ChangeMeClient/0.1 by YourUsername"}
    client_auth = requests.auth.HTTPBasicAuth(client_id, client_secret)
    post_data = {'grant_type': 'password', 'username': USERNAME, 'password': PASSWORD}
    headers = {"User-Agent": "test script by /u/" + USERNAME}
    response = requests.post("https://www.reddit.com/api/v1/access_token", auth=client_auth, data=post_data, headers=headers)
    credentials = json.loads(response.text)
    # print(credentials)
    return(credentials)


def make_reddit_request():  ## ---> if cache dict is empty, make new request
    creds = get_reddit_creds() ## because cache_dict is empty, get reddit credentials and make new request
    headers = {"Authorization": "bearer " + creds["access_token"], "User-Agent": "subreddit top scores script by /u/" + username}
    params = {}
    response2 = requests.get("https://oauth.reddit.com/" + "top", headers=headers, params = {'sort': 'top','limit': 30})
    # for i in json.loads(response2.text):
    #     print(i)
    response_text = json.loads(response2.text)
    # print("response_text")
    # print(response_text)
    cache_file = open(CACHE_FNAME,"w")
    cache_string = json.dumps(response_text)
    print("===================")
    print("THIS IS MY CACHE STRING AND TYPE")
    # print(cache_string)
    # print(type(cache_string))
    cache_file.write(cache_string)
    print("GOT HERE")
    cache_file.close()
    return response_text



# loaded_cache = load_cache()   ## returns a CACHE_Diction either way ##--> this is something to do when start the program 
# ##if the time stamp is too old, then 

# make = make_reddit_request(loaded_cache)



def populate_reddit_db(reddit_request):   ## will need to read it from a cache file either way. 
    print(CACHE_DICTION)
    conn = sqlite.connect(DBNAME)
    cur = conn.cursor()

    for rr in reddit_request["data"]["children"]:
        result = rr["data"]
        # print(result["subreddit"])
        Subreddit_Id = result["subreddit_id"]
        Subreddit_Name = result["subreddit"]
        # Post_Title = result["selftext"]
        Post_Id = result["id"]
        subreddit_subscribers = result["subreddit_subscribers"]
        Thread_Title = result["title"]
        Pinned_content = result["pinned"]
        Original_Content = result["is_original_content"]
        Contains_video = result["is_video"]
        Number_Upvotes = result["ups"]

        insert_statement = '''
            INSERT INTO PostContent(Subreddit_Id, Subreddit_Name, Post_Id, subreddit_subscribers, Thread_Title, Pinned_content, Original_Content, Contains_video) VALUES (?,?,?,?,?,?,?,?)
            ''' 
        cur.execute(insert_statement, [Subreddit_Id, Subreddit_Name, Post_Id, subreddit_subscribers, Thread_Title, Pinned_content, Original_Content, Contains_video])
        conn.commit()

    conn.close()



loaded_cache = load_cache() 

print(loaded_cache.keys())
# loaded_cache = {}
# loaded_cache = {SOME PREVIOUS DATA}
if len(loaded_cache.keys()) > 0: 

    print("--------------")
    loaded_cache = make_reddit_request()

print(loaded_cache.keys())
#


##just got rid of april 17
# reddit_request = make_reddit_request(loaded_cache)


# cache_data(reddit_request)
# populate_reddit_db(reddit_request)



##### NOT USING!!! #####
# class Post():
#     def __init__(self):
#         self.


# link_flair_type
# media 
#    #(true or false)

# ["ups"]





    # cur.execute('''CREATE TABLE IF NOT EXISTS PostVotes(
    #             "ID" SERIAL PRIMARY KEY,
    #             "Post_Id" TEXT NOT NULL,
    #             "Subcategory_Name" TEXT NOT NULL,
    #             "Subcategory_Id" INTEGER NOT NULL,
    #             "Number_Upvotes" INTEGER NOT NULL,
    #             "Number_Downvotes" INTEGER NOT NULL)
    #             ''')








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


