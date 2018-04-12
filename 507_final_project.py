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
        "Subreddit_name" TEXT,
        "Subreddit_Id" TEXT,
        "subreddit_subscribers" TEXT,
        "Thread_Title" TEXT,
        "Post_Title" TEXT,        
        "Pinned_content" TEXT,
        "Original_Content" TEXT,
        "Contains_video" TEXT
        )'''

        # "Post_Date" TEXT,

        # "Contains_link" NUMERIC NOT NULL

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


#  Saves cache contents into a json file
def save_cache():
    full_text = json.dumps(CACHE_DICTION)
    cache_file_ref = open(CACHE_FNAME,"w")
    cache_file_ref.write(full_text)
    cache_file_ref.close()
    pass

#  Gets the saved token from the cache

#  Loads cache into global CACHE_DICTION
# def load_cache():
#     global CACHE_DICTION
#     try:
#         cache_file = open(CACHE_FNAME, 'r')
#         cache_contents = cache_file.read()
#         CACHE_DICTION = json.loads(cache_contents)
#         cache_file.close()
#         cur.execute("DELETE FROM Postings")
#         conn.commit()
#         if check_cache_time():
#             CACHE_DICTION = {}
#             os.remove('cache_contents.json')
#     except:
#         CACHE_DICTION = {}


# def get_saved_token():
#     with open(CACHE_CREDS, 'r') as creds:
#         token_json = creds.read()
#         token_dict = json.loads(token_json)
#         return token_dict['access_token']

# #  Saves token from authentication
# def save_token(token_dict):
#     with open(CACHE_CREDS, 'w') as creds:
#         token_json = json.dumps(token_dict)
#         creds.write(token_json)

# #  Checks token file if older than 1 hour
# def check_token_time():
#     t = os.path.getctime('creds.json')
#     created_time = datetime.fromtimestamp(t)
#     now = datetime.now()

#     # subtracting two datetime objects gives you a timedelta object
#     delta = now - created_time
#     delta_in_seconds = delta.seconds

#     # now that we have seconds as integers, we can just use comparison
#     # and decide if the token has expired or not
#     if delta_in_seconds <= 3600:
#         return False
#     else:
#         return True



def get_reddit_creds():
    pass

    headers = {"Authorization": "bearer fhTdafZI-0ClEzzYORfBSCR7x3M", "User-Agent": "ChangeMeClient/0.1 by YourUsername"}

    client_auth = requests.auth.HTTPBasicAuth(client_id, client_secret)
    post_data = {'grant_type': 'password', 'username': USERNAME, 'password': PASSWORD}
    headers = {"User-Agent": "test script by /u/" + USERNAME}
    response = requests.post("https://www.reddit.com/api/v1/access_token", auth=client_auth, data=post_data, headers=headers)
    credentials = json.loads(response.text)
    print(credentials)
    return(credentials)





def make_reddit_request(credentials):
    headers = {"Authorization": "bearer " + creds["access_token"], "User-Agent": "subreddit top scores script by /u/" + username}
    params = {}
    response2 = requests.get("https://oauth.reddit.com/" + "top", headers=headers, params = {'sort': 'top','limit': 4})
    # for i in json.loads(response2.text):
    #     print(i)
    return json.loads(response2.text)




create_reddit_db()
populate_reddit_db()
creds = get_reddit_creds()
reddit_request = make_reddit_request(creds)



for rr in reddit_request["data"]["children"]:
    result = rr["data"]
    # print(result["subreddit"])
    Subcategory_Id = result["subreddit_id"]
    Subcategory_Name = result["subreddit"]
    Post_Title = result["selftext"]
    Subreddit_name = result["subreddit"]
    Subreddit_Id = result["subreddit_id"]
    subreddit_subscribers = result["subreddit_subscribers"]
    Thread_Title = result["title"]
    Post_Id = result["id"]
    Pinned_content = result["pinned"]
    Original_Content = result["is_original_content"]
    Contains_video = result["is_video"]







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


