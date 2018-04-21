import sqlite3 as sqlite3

import plotly.plotly as py
# from plotly.graph_objs import *
import plotly.graph_objs as go


DBNAME = '507_reddit_final.db'


# # def process_command(response):

# conn = sqlite3.connect(DBNAME)
# cur = conn.cursor()    


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
                most_represented_categories()

            elif response[0] in ['overlap']:
                overlap_categories_listings()

            elif response[0] in ['listings']:
                listing_titles_number_comments()

            else:
                has_video()

            print("\n")
            response = user_query()

    except:
        print("\n")
        response = user_query()

    if response[0] == 'exit':
        print('bye!')
        exit()




#####################################################################################
## To see the 10 most represented categories of subreddits in the "Top" results

def most_represented_categories():
    conn = sqlite3.connect(DBNAME)
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

most_represented_categories()

##############################################################################################
##correlation between subreddit category of top posts and how many subscribers they have
## the subreddit category of the top posts of the days, against how many subscribers that category has  ##

def overlap_categories_listings():
    conn = sqlite3.connect(DBNAME)
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
    conn = sqlite3.connect(DBNAME)
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
    conn = sqlite3.connect(DBNAME)
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
    # print(no_video)
    labels = ['Contains a Video','Does not contain a Video']
    values = [the_result, no_video]

    trace = go.Pie(labels=labels, values=values)
    py.plot([trace], filename='basic_pie_chart')


# interactive_prompt()
