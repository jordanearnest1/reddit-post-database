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

DBNAME = '507_final_reddit_2_hide_vpn.db'
CACHE_FNAME = 'reddit_cache_trying_hide_vpn1.json'
SUBREDDIT_CACHE = "subreddit_detail_cache_hide_vpn3.json"


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
        "Subreddit_Name_Prefixed" TEXT,
        "Listing_title" TEXT,
        "Author" TEXT,
        "Contains_video" TEXT,
        "Number_Upvotes" INTEGER,
        "Listing_URL" TEXT,
        "Number_Comments" INTEGER
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
                    "Subreddit_Name" TEXT,
                    "Subreddit_Name_Prefixed" TEXT,
                    "subreddit_subscribers" INTEGER,
                    "Subreddit_description" TEXT,
                    "Audience_category" TEXT)
                    ''')

    conn.commit()
    conn.close()

def check_if_cache_exists(cache_file_name):
    try:
        with open(cache_file_name, "r", encoding= 'utf-8') as cache_file:
                cache_string = cache_file.read()
        print("cache already exists, loading cache")
        return True

    except:
        with open(cache_file_name, "w", encoding= 'utf-8') as cache_file:
            cache_file.write("")
        print("created new cache file, loading cache")
        return False

def load_cache(cache_file_name):
    # global CACHE_FNAME

    check_cache = check_if_cache_exists(cache_file_name) 
    if check_cache is True:
        with open(cache_file_name, "r", encoding= 'utf-8') as cache_file:
            cache_string = cache_file.read()
            if cache_file_name in [CACHE_FNAME]:   ## if we are looking at the main cache file
                print("if statemetn in check cache false")
                CACHE_DICTION = json.loads(cache_string)
                return CACHE_DICTION
            else:  ##meaning, if we are looking at the subreddit cache file
                print("else statement in check cache false")
                SUBREDDIT_DICTION = json.loads(cache_string)
                return SUBREDDIT_DICTION
    else:
        if cache_file_name in [CACHE_FNAME]:
            print("if statement in check cache true")
            CACHE_DICTION = {}
            return CACHE_DICTION
        else:
            print("else statement in check cache true")
            SUBREDDIT_DICTION = {}
            return SUBREDDIT_DICTION

#  Saves cache contents into a json file
def write_cache_data(data_to_cache, cache_file_name):
    # full_text = json.dumps(CACHE_DICTION)
    cache_file = open(cache_file_name,"w", encoding ='utf-8')
    cache_string = json.dumps(data_to_cache)
    cache_file.write(cache_string)
    cache_file.close()


def get_reddit_creds():
    # headers = {"Authorization": "bearer fhTdafZI-0ClEzzYORfBSCR7x3M", "User-Agent": "ChangeMeClient/0.1 by YourUsername"}
    client_auth = requests.auth.HTTPBasicAuth(client_id, client_secret)
    post_data = {'grant_type': 'password', 'username': USERNAME, 'password': PASSWORD}
    headers = {"User-Agent": "https://www.programsinformationpeople.org/runestone/static/publicPIP/ (by/u/saraliebman)"}
    response = requests.post("https://www.reddit.com/api/v1/access_token", auth=client_auth, data=post_data, headers = headers)
    response.raise_for_status()
    # headers=headers
    token = response.json()
    # credentials = json.loads(response.text)
    print(token)

    # headers = {'Authorization': 'Bearer ' + token, "User-Agent": "http://www.kzoo.edu v1.2.3 (by/u/jordanearnest)"}
    # response = requests.get("https://oauth.reddit.com/api/v1/me", headers=headers)
    # response.raise_for_status()

    return(token)

#get_reddit_creds()


# {'access_token': '95981440222-MEghZSvMQTzuo6ewBDqwqN11Wd8', 'token_type': 'bearer', 'expires_in': 3600, 'scope': '*'}


def make_reddit_request(cache_file_name, Subreddit_Name_Prefixed = ""):  ## ---> if cache dict is empty, make new request
    current_time = datetime.now()
    yesterday = current_time -timedelta(1)
    # creds = get_reddit_creds() ## because cache_dict is empty, get reddit credentials and make new request

    headers = {"Authorization": "bearer 95981440222-MEghZSvMQTzuo6ewBDqwqN11Wd8", "User-Agent": "https://www.programsinformationpeople.org/runestone/static/publicPIP/ (by/u/saraliebman)"}
    # headers = {"Authorization": "bearer " + creds["access_token"], "User-Agent": 'your bot 0.1'}

    params = {}
    if cache_file_name in [CACHE_FNAME]:
        print("doing the if statement in make_reddit_request")
        response2 = requests.get("https://oauth.reddit.com/" + "top", headers=headers, params = {'sort': 'top', 'before' : current_time, 'limit': 100})

        # response2 = requests.get("https://oauth.reddit.com/r/" + "top", headers=headers, params = {'sort': 'top','limit': 30})

        # with open('debug_out_string.html', 'w', encoding='utf-8') as debug:
        #     debug.write(response2.text)
        response_text = json.loads(response2.text, encoding ='utf-8')

    else:
        print("doing the else statement in make_reddit_request, this should only happen when getting subreddit cache")
        print(Subreddit_Name_Prefixed)
        response2 = requests.get("https://reddit.com/" + Subreddit_Name_Prefixed[0] + "/about.json")
        response_text = json.loads(response2.text)

    write_cache_data(response_text, cache_file_name)   ####----> Need to put this back in!
    print("writing data into the cache...")
    # print(write_cache_data)

    return response_text
##headers=headers, params = {'sort': 'top', 'limit': 30}

# loaded_cache = load_cache()   ## returns a CACHE_Diction either way ##--> this is something to do when start the program 
# ##if the time stamp is too old, then 


def populate_db_main_table(cache_file= CACHE_FNAME):   ## will need to read it from a cache file either way. 
    loaded_cache = load_cache(CACHE_FNAME)

    conn = sqlite.connect(DBNAME)
    cur = conn.cursor()
    print(loaded_cache)
    count = 0
    for rr in loaded_cache["data"]["children"]:
        print("count = " )
        print(count)
        a_result = rr["data"]

        Subreddit_Name_Prefixed = a_result["subreddit_name_prefixed"]   ### did i add this above?!
        Listing_title = a_result["title"] 
        Author = a_result["author"]
        Contains_video = a_result["is_video"] ## ^
        Number_Upvotes = a_result["ups"] ##^
        Listing_URL= a_result["url"] ## NEED TO ADD ABOVE
        Number_Comments = a_result["num_comments"]  ##--> NEED TO ADD ABOVE

        count += 1
        post_insert_statement = '''
            INSERT INTO PostContent(Subreddit_Name_Prefixed, Listing_title, Author, Contains_video, Number_Upvotes, Listing_URL, Number_Comments) VALUES (?,?,?,?,?,?,?)
            ''' 
        cur.execute(post_insert_statement, [Subreddit_Name_Prefixed, Listing_title, Author, Contains_video, Number_Upvotes, Listing_URL, Number_Comments])
        conn.commit()

    conn.close()



def populate_db_sub_table(cache_file = SUBREDDIT_CACHE):
    conn = sqlite.connect(DBNAME)
    cur = conn.cursor()    
    statement = '''
        SELECT DISTINCT Subreddit_Name_Prefixed,
            COUNT(Subreddit_Name_Prefixed) AS occurence
        FROM PostContent
        GROUP BY Subreddit_Name_Prefixed
        ORDER BY occurence DESC
        LIMIT 50
    '''
    cur.execute(statement)    
    results = cur.fetchall()

    lst_50_top_subreddit_prefixes = []
    
    for r in results:
        lst_50_top_subreddit_prefixes.append(r)

    loaded_cache = load_cache(SUBREDDIT_CACHE)

    for Subreddit_Name_Prefixed in lst_50_top_subreddit_prefixes:
        if Subreddit_Name_Prefixed in loaded_cache:
            Subreddit_Id = a_result["id"] 
            Subreddit_Name = a_result["subreddit"] 
            subreddit_subscribers = Subreddit_Id["subscribers"]
            Subreddit_description = Subreddit_Id["public_description"]
            Audience_category = Subreddit_Id["audience_target"]
        else: 
            another_result_request = make_reddit_request(SUBREDDIT_CACHE, Subreddit_Name_Prefixed)
            another_result = load_cache(SUBREDDIT_CACHE)
            print("this is made reddit request")
            # print(another_result)
            # for a_result in another_result["data"]:

            #     Subreddit_Id = a_result["id"] 
            #     Subreddit_Name = a_result["subreddit"] 
            #     subreddit_subscribers = Subreddit_Id["subscribers"]
            #     Subreddit_description = Subreddit_Id["public_description"]
            #     Audience_category = Subreddit_Id["audience_target"]

            a_result = another_result["data"]
            Subreddit_Id = a_result["id"] 
            Subreddit_Name = a_result["display_name"] 
            subreddit_subscribers = a_result["subscribers"]
            Subreddit_description = a_result["public_description"]
            Audience_category = a_result["audience_target"]

        subreddit_insert_statement = '''
            INSERT INTO Subreddit_Table(Subreddit_Id, Subreddit_Name, Subreddit_Name_Prefixed, subreddit_subscribers, Subreddit_description, Audience_category) VALUES (?,?,?,?,?,?)
            ''' 
        cur.execute(subreddit_insert_statement, [Subreddit_Id, Subreddit_Name, Subreddit_Name_Prefixed, subreddit_subscribers, Subreddit_description, Audience_category])
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

# create_reddit_db()



############### apr 19, 8:38, this is what's up ##################

# create_reddit_db()
# load_cache(CACHE_FNAME)

# make_reddit_request(CACHE_FNAME)
# lc = load_cache(CACHE_FNAME)

# populate_db_main_table()

populate_db_sub_table("subreddit_detail_cache_hide_vpn1.json")

#############################

# another_result = load_cache("subreddit_detail_cache_hide_vpn1.json")
# print("this is made reddit request")
# # print(another_result)
# a_result = another_result["data"]

# # for x in a_result:
# #     print(x)


# Subreddit_Id = a_result["id"] 
# Subreddit_Name = a_result["display_name"] 
# subreddit_subscribers = a_result["subscribers"]
# Subreddit_description = a_result["public_description"]
# Audience_category = a_result["audience_target"]

# print(Subreddit_Id, Subreddit_Name, subreddit_subscribers, Subreddit_description, Audience_category)

