import sqlite3 as sqlite
import csv
import json
from bs4 import BeautifulSoup
import requests
import requests.auth
from datetime import *
from reddit_secrets import *
import os
import plotly.plotly as py
from plotly.graph_objs import *

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
        "subreddit_subscribers" TEXT,
        "Subreddit_description" TEXT,
        "Audience_category" TEXT
        )'''
    cur.execute(create_table_one)
    conn.commit()



    statement = '''
        DROP TABLE IF EXISTS "Subreddit_Table";
    ''' 
    cur.execute(statement)
    conn.commit()
    cur.execute('''CREATE TABLE IF NOT EXISTS Subreddit_Table(
                    "Subreddit_Id" TEXT,
                    "Listing_title" TEXT,
                    "Pinned_content" TEXT,
                    "Original_Content" TEXT,
                    "Contains_video" TEXT,
                    "Number_Upvotes" INTEGER NOT NULL,
                    "Number_Downvotes" INTEGER,
                    "Number_Comments" INTEGER)
                    ''')
                # "ID" SERIAL PRIMARY KEY,
                # "Post_Id" TEXT NOT NULL,
                # "Subcategory_Name" TEXT NOT NULL,
                # "Subcategory_Id" INTEGER NOT NULL,
                # "Number_Upvotes" INTEGER NOT NULL,
                # "Number_Downvotes" INTEGER NOT NULL)
                # ''')
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
        print("CHECK CACHE IN LOAD CACHE IS FALSE")
        with open(CACHE_FNAME, "r") as cache_file:
            cache_string = cache_file.read()
            CACHE_DICTION = json.loads(cache_string)
        return CACHE_DICTION
    else:
        CACHE_DICTION = {}
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
    current_time = datetime.now()
    yesterday = now = timedelta(1)
    creds = get_reddit_creds() ## because cache_dict is empty, get reddit credentials and make new request
    headers = {"Authorization": "bearer " + creds["access_token"], "User-Agent": "subreddit top scores script by /u/" + username}
    params = {}
    response2 = requests.get("https://oauth.reddit.com/" + "top", headers=headers, params = {'sort': 'top', 'before' : current_time, 'after': yesterday,'limit': 30})

    response_text = json.loads(response2.text)
    write_cache_data(response_text)   ####----> Need to put this back in!
    print("this is the type of the response")
    print(type(response_text))
    # cache_file = open(CACHE_FNAME,"w")
    # cache_string = json.dumps(response_text)
    # cache_file.write(cache_string)
    # cache_file.close()
    return response_text


# loaded_cache = load_cache()   ## returns a CACHE_Diction either way ##--> this is something to do when start the program 
# ##if the time stamp is too old, then 



def populate_reddit_db(cache_dict):   ## will need to read it from a cache file either way. 
    # print(CACHE_DICTION)
    conn = sqlite.connect(DBNAME)
    cur = conn.cursor()

    for rr in reddit_request["data"]["children"]:
        a_result = rr["data"]

        Listing_title = a_result["title"]  #listing title  ^ ##used to be thread title
        Pinned_content = a_result["pinned"]
        Original_Content = a_result["is_original_content"] ## ^
        Contains_video = a_result["is_video"] ## ^
        Number_Upvotes = a_result["ups"] ##^
        Number_Downvotes= a_result["downs"] ## NEED TO ADD ABOVE
        Number_Comments = a_result["num_comments"]  ##--> NEED TO ADD ABOVE


        Subreddit_Id = a_result["id"] 
        Subreddit_Name = a_result["subreddit"]  
        subreddit_subscribers = a_result["subscribers"]
        Subreddit_description = a_result["public_description"]
        Audience_category = a_result["audience_target"]


        post_insert_statement = '''
            INSERT INTO PostContent(Subreddit_Id, Listing_title, Pinned_content, Original_Content, Contains_video, Number_Upvotes, Number_Downvotes, Number_Comments) VALUES (?,?,?,?,?,?,?,?)
            ''' 
        cur.execute(post_insert_statement, [Subreddit_Id, Listing_title, Pinned_content, Original_Content, Contains_video, Number_Upvotes, Number_Downvotes, Number_Comments])
        conn.commit()


        subreddit_insert_statement = '''
            INSERT INTO Subreddit_Table(Subreddit_Id, Subreddit_Name, subreddit_subscribers, Subreddit_description, Audience_category) VALUES (?,?,?,?,?)
            ''' 
        cur.execute(subreddit_insert_statement, [Subreddit_Id, Subreddit_Name, subreddit_subscribers, Subreddit_description, Audience_category])
        conn.commit()


    conn.close()

#### pasting to reference the order

### will need to insert subreddit id in both!!



## for now while i try out getting the results
##create_reddit_db()


## commented out april 18, 1:09pm
# loaded_cache = load_cache()   ## Returns a cache diction
# print("this is the type")
# print(type(loaded_cache))
# print(loaded_cache.keys())



# loaded_cache = {}
# loaded_cache = {SOME PREVIOUS DATA}

#### will need this again later  ####
# if len(loaded_cache.keys()) > 0: ## meaning, if i have emptied my cach
#     print("--------------")
#     print("the length of my cache diction keys is: ")
#     print(len(loaded_cache.keys()))
#     loaded_cache = make_reddit_request()
#     print("THIS Is the type of my loaded cache")
#     print(type(loaded_cache))
# else:
#     print("here, went to else")


# for r in loaded_cache["data"]["children"]:
#     rr = r["data"]["pinned"]
#     print(rr)
#         # print(x)
#     print("==============")





make = make_reddit_request()

for r in make["data"]:
    print(r)


for r in make["data"]["after"]:
    print(r)

for r in make["data"]["dist"]:
    print(r)

    print("============")

for r in make["data"]["modhash"]:
    print(r)

    print("============")

for r in make["data"]["whitelist_status"]:
    print(r)


for r in make["data"]["children"]:
    print(r)

for r in make["data"]["before"]:
    print(r)



for rr in make["data"]["children"]:
    a_result = rr["data"]

    Listing_title = a_result["title"]  #listing title  ^ ##used to be thread title
    Pinned_content = a_result["pinned"]
    Original_Content = a_result["is_original_content"] ## ^
    Contains_video = a_result["is_video"] ## ^
    Number_Upvotes = a_result["ups"] ##^
    Number_Downvotes= a_result["downs"] ## NEED TO ADD ABOVE
    Number_Comments = a_result["num_comments"]  ##--> NEED TO ADD ABOVE


    Subreddit_Id = a_result["id"] 
    Subreddit_Name = a_result["subreddit"]  
    #subreddit_subscribers = a_result["subscribers"]
    #Subreddit_description = a_result["public_description"]
    #Audience_category = a_result["audience_target"]

   # print(Listing_title, Pinned_content, Original_Content, Contains_video, Number_Upvotes, Number_Downvotes, Number_Comments, Subreddit_Id, Subreddit_Name, )


# subreddit_subscribers, Subreddit_description, Audience_category