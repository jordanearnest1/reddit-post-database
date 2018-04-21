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
import plotly.graph_objs as go
import unittest

CLIENT_ID = client_id
CLIENT_SECRET = client_secret
PASSWORD = password
USERNAME = username

DBNAME = '507_reddit_final.db'
CACHE_FNAME = 'reddit_cache_trying_hide_vpn1.json'



####################################################################
#################### CONNECT TO and CREATE DATABASE ###############
####################################################################

def create_reddit_db():
    try:
        conn = sqlite.connect(DBNAME)
        cur = conn.cursor()
    except:
        print("Could not connect to initial cursor. Try again.")




    ## CREATING PostContent TABLE
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



    ## CREATING SUBREDDIT TABLE
    statement = '''
        DROP TABLE IF EXISTS "Subreddit_Table";
    ''' 
    cur.execute(statement)
    conn.commit()
    cur.execute('''
        CREATE TABLE IF NOT EXISTS Subreddit_Table(
            "Subreddit_Id" TEXT,
            "Subreddit_Name" TEXT,
            "Subreddit_Name_Prefixed" TEXT,
            "subreddit_subscribers" INTEGER)
            ''')

    conn.commit()



    ###CREATING TodayRedditStats TABLE
    statement = '''
        DROP TABLE IF EXISTS 'TodayRedditStats';
    ''' 
    cur.execute(statement)
    conn.commit()
    create_table_one = '''
        CREATE TABLE "TodayRedditStats"(
        "ID" INTEGER PRIMARY KEY AUTOINCREMENT,

        "Today_Most_Popular_Subreddit_Name" TEXT,
        "Today_Most_Popular_Subreddit_Rank" INTEGER

        )'''
    cur.execute(create_table_one)
    conn.commit()



    ###CREATING All_TimeRedditStats TABLE
    statement = '''
        DROP TABLE IF EXISTS 'All_TimeRedditStats';
    ''' 
    cur.execute(statement)
    conn.commit()
    create_table_one = '''
        CREATE TABLE "All_TimeRedditStats"(
        "ID" INTEGER PRIMARY KEY AUTOINCREMENT,

        "All_time_most_subscribed_name" TEXT,
        "All_time_most_subscribed_rank" INTEGER

        )'''
    cur.execute(create_table_one)
    conn.commit()




    ###CREATING Growing_RedditStats TABLE
    statement = '''
        DROP TABLE IF EXISTS 'Growing_RedditStats';
    ''' 
    cur.execute(statement)
    conn.commit()
    create_table_one = '''
        CREATE TABLE "Growing_RedditStats"(
        "ID" INTEGER PRIMARY KEY AUTOINCREMENT,
        "Today_Most_Growing_Subreddit_Name" TEXT,
        "Today_Most_Growing_Subreddit_Rank" INTEGER

        )'''
    cur.execute(create_table_one)
    conn.commit()
    conn.close()




############################################################################################
########################################### CACHE FUNCTIONS ################################
#############################################################################################

def check_if_cache_exists(cache_file_name):
    try:
        with open(cache_file_name, "r", encoding= 'utf-8') as cache_file:
                cache_string = cache_file.read()
        return True

    except:
        with open(cache_file_name, "w", encoding= 'utf-8') as cache_file:
            cache_file.write("")
        return False

def load_cache(cache_file_name):
    check_cache = check_if_cache_exists(cache_file_name) 
    if check_cache is True:
        with open(cache_file_name, "r", encoding= 'utf-8') as cache_file:
            cache_string = cache_file.read()
            if cache_file_name in [CACHE_FNAME]:   ## if we are looking at the main cache file
                CACHE_DICTION = json.loads(cache_string)
                return CACHE_DICTION
            else:  ##meaning, if we are looking at the subreddit cache file
                SUBREDDIT_DICTION = json.loads(cache_string)
                return SUBREDDIT_DICTION
    else:
        if cache_file_name in [CACHE_FNAME]:
            CACHE_DICTION = {}
            return CACHE_DICTION
        else:
            SUBREDDIT_DICTION = {}
            return SUBREDDIT_DICTION

def write_cache_data(data_to_cache, cache_file_name):
    # full_text = json.dumps(CACHE_DICTION)
    cache_file = open(cache_file_name,"w", encoding ='utf-8')
    cache_string = json.dumps(data_to_cache)
    cache_file.write(cache_string)
    cache_file.close()


###################################################################################################
######################################## REQUEST FUNCTIONS #######################################
###################################################################################################

def get_reddit_creds():
    client_auth = requests.auth.HTTPBasicAuth(client_id, client_secret)
    post_data = {'grant_type': 'password', 'username': USERNAME, 'password': PASSWORD}
    headers = {"User-Agent": "https://www.programsinformationpeople.org/runestone/static/publicPIP/ (by/u/saraliebman)"}
    response = requests.post("https://www.reddit.com/api/v1/access_token", auth=client_auth, data=post_data, headers = headers)
    token = response.json()
    return token

def make_reddit_request(cache_file_name, Subreddit_Name_Prefixed = ""):
    current_time = datetime.now()
    creds = get_reddit_creds() ## because cache_dict is empty, get reddit credentials and make new request
    headers = {"Authorization": "bearer " + creds["access_token"], "User-Agent": 'umsi final project'}
    params = {}
    response2 = requests.get("https://oauth.reddit.com/" + "top", headers=headers, params = {'sort': 'top', 'before' : current_time, 'limit': 100})
    response_text = json.loads(response2.text, encoding='utf-8')

    write_cache_data(response_text, cache_file_name)  
    # return response_text


def make_redditlst_request_using_cache(unique_url):
    CACHE_FNAME = '507_final_scraped.json'
    try:
        cache_file_name = open(CACHE_FNAME, 'r')
        cache_contents_string = cache_file_name.read()
        CACHE_DICTION = json.loads(cache_contents_string)
        cache_file_name.close()
    except:
        CACHE_DICTION = {}


    if unique_url in CACHE_DICTION:
        return CACHE_DICTION[unique_url]  ##access existing data

    else: 
        resp = requests.get(unique_url)
        CACHE_DICTION[unique_url] = resp.text # only store the html
        dumped_json_cache = json.dumps(CACHE_DICTION)
        fw = open(CACHE_FNAME,"w")
        fw.write(dumped_json_cache)  ##caching full text from webpage
        fw.close() # Close the open file
        return CACHE_DICTION[unique_url]




#################################################################################################
################################## Populate Database FUNCTIONS ################################
#################################################################################################

def populate_db_main_table(cache_file= CACHE_FNAME):   ## will need to read it from a cache file either way. 
    loaded_cache = load_cache(CACHE_FNAME)

    conn = sqlite.connect(DBNAME)
    cur = conn.cursor()
    count = 0
    for rr in loaded_cache["data"]["children"]:
        a_result = rr["data"]
        Subreddit_Name_Prefixed = a_result["subreddit_name_prefixed"]   ### did i add this above?!
        Listing_title = a_result["title"] 
        Author = a_result["author"]
        Contains_video = a_result["is_video"] ## ^
        Number_Upvotes = a_result["ups"] ##^
        Listing_URL= a_result["url"] ## NEED TO ADD ABOVE
        Number_Comments = a_result["num_comments"]  ##--> NEED TO ADD ABOVE

        Subreddit_Id = a_result["subreddit_id"] 
        Subreddit_Name = a_result["subreddit"] 
        subreddit_subscribers = a_result["subreddit_subscribers"] 

        post_insert_statement = '''
            INSERT INTO PostContent(Subreddit_Name_Prefixed, Listing_title, Author, Contains_video, Number_Upvotes, Listing_URL, Number_Comments) VALUES (?,?,?,?,?,?,?)
            ''' 
        cur.execute(post_insert_statement, [Subreddit_Name_Prefixed, Listing_title, Author, Contains_video, Number_Upvotes, Listing_URL, Number_Comments])
        conn.commit()

        subreddit_insert_statement = '''
            INSERT INTO Subreddit_Table(Subreddit_Id, Subreddit_Name, Subreddit_Name_Prefixed, subreddit_subscribers) VALUES (?,?,?,?)
            ''' 
        cur.execute(subreddit_insert_statement, [Subreddit_Id, Subreddit_Name, Subreddit_Name_Prefixed, subreddit_subscribers])
        conn.commit()

    conn.close()


def get_redditlist_info():  
    redditlist_cache = make_redditlst_request_using_cache("http://redditlist.com/")
    redditlist_soup = BeautifulSoup(redditlist_cache, "html.parser")
    content_div = redditlist_soup.find(class_ = "listing-container")  ## will then look at each "span 4 listing"
    categories = content_div.find_all(id= "listing-parent")
    
    conn = sqlite.connect(DBNAME)
    cur = conn.cursor()


    for a_category in categories:  ### isolates each of the groups of categories
        for c in a_category:
            try:
                category_name = c.find("h3").text
            except:
                category_name = None
            redditlist_mini_dict = {}
            if category_name == "Recent Activity":  

                item = a_category.find_all(class_= "listing-item")
                for a in item:     ##isolating a single reddit listing
                    Today_Most_Popular_Subreddit_Name = a.find("a").text
                    Today_Most_Popular_Subreddit_Rank= a.find(class_= "rank-value").text
                    insert_statement = '''
                        INSERT INTO TodayRedditStats(
                            Today_Most_Popular_Subreddit_Name, Today_Most_Popular_Subreddit_Rank)
                            VALUES (?, ?)
                    ''' 
                    cur.execute(insert_statement, [Today_Most_Popular_Subreddit_Name, Today_Most_Popular_Subreddit_Rank])
                    conn.commit()
                    # conn.close()


            elif category_name == "Subscribers":
                item = a_category.find_all(class_= "listing-item")
                for a in item:     ##isolating a single reddit listing
                    All_time_most_subscribed_name = a.find("a").text
                    All_time_most_subscribed_rank= a.find(class_= "rank-value").text
                    # conn = sqlite.connect(DBNAME)
                    # cur = conn.cursor()
                    insert_statement = '''
                        INSERT INTO All_TimeRedditStats(
                            All_time_most_subscribed_name, All_time_most_subscribed_rank)
                            VALUES (?, ?)
                    ''' 
                    cur.execute(insert_statement, [All_time_most_subscribed_name, All_time_most_subscribed_rank])
                    conn.commit()
                    # conn.close()

        
            elif category_name == "Growth (24Hrs)":
                item = a_category.find_all(class_= "listing-item")
                for a in item:     ##isolating a single reddit listing
                    Today_Most_Growing_Subreddit_Name = a.find("a").text
                    Today_Most_Growing_Subreddit_Rank= a.find(class_= "rank-value").text
                    # conn = sqlite.connect(DBNAME)
                    # cur = conn.cursor()
                    insert_statement = '''
                        INSERT INTO Growing_RedditStats(
                            Today_Most_Growing_Subreddit_Name, Today_Most_Growing_Subreddit_Rank)
                            VALUES (?, ?)
                    ''' 
                    cur.execute(insert_statement, [Today_Most_Growing_Subreddit_Name, Today_Most_Growing_Subreddit_Rank])
                    conn.commit()

            else:
                pass

    conn.close()





###################################################################################################
######################################### Visualizations FUNCTIONS ################################
###################################################################################################


## To see the 10 most represented categories of subreddits in the "Top" results
def most_represented_categories():
    conn = sqlite.connect(DBNAME)
    cur = conn.cursor()    

    statement = '''
        SELECT st.Subreddit_Name, count(pc.Listing_title)
        FROM PostContent as pc
            Join Subreddit_Table as st
            ON pc.Subreddit_Name_Prefixed = st.Subreddit_Name_Prefixed
        GROUP BY st.Subreddit_Name
        LIMIT 10
        '''
    cur.execute(statement)    
    results = cur.fetchall()

    label_lst = []
    count_lst = []

    for result in results:
        label_lst.append(result[0])
        count_lst.append(result[1])

    labels = label_lst
    values = count_lst
    colors = ['#FEBFB3', '#E1396C', '#96D38C', '#D0F9B1', "#bfb3fe", '#feb3cd', "#b3f2fe", "#fd679b", "#fd81eb", "#b3cefe"]

    trace = go.Pie(labels=labels, values=values,
                   hoverinfo='label+value', textinfo='label', 
                   textfont=dict(size=18),
                   marker=dict(colors=colors, 
                               line=dict(color='#000000', width=2)))
    py.plot([trace], filename='styled_pie_chart')


##correlation between subreddit category of top posts and how many subscribers they have
## the subreddit category of the top posts of the days, against how many subscribers that category has  ##
def overlap_categories_listings():
    conn = sqlite.connect(DBNAME)
    cur = conn.cursor()    

    statement = '''
        SELECT DISTINCT Subreddit_Name, subreddit_subscribers
        FROM Subreddit_Table
        ORDER BY subreddit_subscribers DESC
        LIMIT 10
        '''

    cur.execute(statement)    
    results = cur.fetchall()

    return_lst = []

    subreddit_label_lst = []
    subreddit_subscriber_lst = []


    for result in results:
        subreddit_label_lst.append(result[0])
        subreddit_subscriber_lst.append(int(result[1]))


    ###how many of today's top posts fall under each of these subreddit categories
    top_post_subreddit_lst = []
    top_post_subreddit_value_lst = []

    statement = '''
        SELECT Subreddit_Name, count(*)
        FROM Subreddit_Table
        WHERE Subreddit_Name IN (
            SELECT DISTINCT Subreddit_Name
            FROM Subreddit_Table
            ORDER BY subreddit_subscribers DESC
            LIMIT 10
             )
        GROUP BY Subreddit_Name
        LIMIT 10
        '''
    cur.execute(statement)    
    results = cur.fetchall()

    for result in results:
        top_post_subreddit_lst.append(result[0])
        top_post_subreddit_value_lst.append(result[1])



    trace1 = {
      "x": subreddit_label_lst, 
      "y": subreddit_subscriber_lst, 
      "name": "Most Subscribed Subreddits", 
      "type": "bar"
    }
    trace2 = {
      "x": top_post_subreddit_lst, 
      "y": top_post_subreddit_value_lst, 
      "name": "Subreddit Representation in Today's Top Listings", 
      "type": "scatter",
      "yaxis": "Number of listings"
    }
    data = go.Data([trace1, trace2])
    layout = {
      "title": "Most Subscribed Subreddits and Their Representation in Today's Top Listings", 
      "yaxis": {"title": "Subreddit Subscribers"}, 
      "yaxis2": {
        "autorange":"True",
        "ticks": "outside",
        "tick0" : 2,

        "overlaying": "y", 
        "side": "right",
        "tickfont": {"color": "rgb(148, 103, 189)"}, 
        "title" : "Number of today's top listings are from each given subreddit", 
        "titlefont": {"color": "rgb(148, 103, 189)"}
      }
    }
    fig = go.Figure(data=data, layout=layout)
    plot_url = py.plot(fig)


## see the top ten listings today and how many up-votes they have
def listing_titles_number_comments():
    conn = sqlite.connect(DBNAME)
    cur = conn.cursor()    

    statement = '''
        SELECT Listing_title, Number_Upvotes
        FROM PostContent
        ORDER BY Number_Upvotes DESC
        LIMIT 10
        '''
    cur.execute(statement)    
    results = cur.fetchall()

    label_lst = []
    count_lst = []

    for result in results:
        label_lst.append(result[0])
        count_lst.append(result[1])

    data = [go.Bar(
                x= label_lst,
                y= count_lst
        )]

    py.plot(data, filename='basic-bar')


### what percent of posts from each have original content or a video in bar chart
def has_video():
    conn = sqlite.connect(DBNAME)
    cur = conn.cursor()    
    statement = '''
    SELECT DISTINCT Listing_title, count(*)
    FROM PostContent
    WHERE Contains_video is 0

    '''

    cur.execute(statement)    
    results = cur.fetchall()   

    for result in results:
        the_result = result[1]

    no_video = 100 - the_result
    labels = ['Contains a Video','Does not contain a Video']
    values = [the_result, no_video]

    trace = go.Pie(labels=labels, values=values)
    py.plot([trace], filename='basic_pie_chart')



################################################ Interactivity FUNCTIONS ################################


def load_help_text():
    with open('help.txt') as f:
        return f.read()

def user_query():
    user_input = input("\n\n\n ***** Welcome to the Subreddit Database! *****\n Please enter a visualization you would like to see.\nYou may chose between 'representation', 'overlap', 'listings' or 'video' (or 'help' for more info): ")
    command = user_input.lower().split()
    return command

def interactive_prompt():
    help_text = load_help_text()

    response = user_query()

    try:
        while response[0] != 'exit':

            if response[0] == 'help':
                print(help_text)
                # continue

            elif response[0] not in ['representation','overlap','listings','video','help','exit']:
                str_response = ""
                for i in response:
                    str_response += i
                    str_response += " "
                print('Command is not recognized: '+ str_response)

            elif response[0] in ['representation']:
                print("Opening visualization in your browser........ ")
                most_represented_categories()

            elif response[0] in ['overlap']:
                print("Opening visualization in your browser........ ")
                overlap_categories_listings()

            elif response[0] in ['listings']:
                print("Opening visualization in your browser........ ")
                listing_titles_number_comments()

            else:
                print("Opening visualization in your browser........ ")
                has_video()

            print("\n")
            response = user_query()

    except:
        print("\n")
        response = user_query()

    if response[0] == 'exit':
        print('bye!')
        exit()







############### RUNNING THE FILE  ##################

# When you first create your database: 
# create_reddit_db()

# # Once a day to delete your cache and get the day's data, run:
# load_cache(CACHE_FNAME)  
# make_reddit_request(CACHE_FNAME)


# # populate the table with today's data 
# lc = load_cache(CACHE_FNAME)
# populate_db_main_table()
# get_redditlist_info()


##### Run the program interaction !#######
interactive_prompt()


