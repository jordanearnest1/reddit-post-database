import sqlite3 as sqlite3

import plotly.plotly as py
# from plotly.graph_objs import *
import plotly.graph_objs as go


DBNAME = '507_final_reddit.db'


# def process_command(response):

conn = sqlite3.connect(DBNAME)
cur = conn.cursor()    

# if len(response) == 1:
#     primary_query = response[0]
#     query_params = ''

# else:
#     primary_query = response[0]
#     query_params = response[1:]

##

##need to add the "if user enters ___ part."

# "PostContent"
# "ID"
# "Subreddit_Id"
# "Subreddit_Name"
# "Post_Id"
# "subreddit_subscribers"

#this will change to something like:

# statement = '''
#     SELECT P.Subreddit_Name
#     FROM PostContent as P
#     JOIN Subreddit_Table as S
#     ON S.Subreddit_Id = P.Subreddit_Id
#     ORDER BY subreddit_subscribers DESC
#     LIMIT 20
# '''


# statement = '''
#     SELECT DISTINCT Subreddit_Name
#     FROM PostContent
#     ORDER BY subreddit_subscribers DESC
#     LIMIT 20
# '''

# cur.execute(statement)
# results = cur.fetchall()

# return_lst = []
# for result in results:
#     print(result)


#####################################################################################
## To see the 10 most represented categories of subreddits in the "Top" results

def most_represented_categories():
    statement = '''
        SELECT Subreddit_Name, count(*)
        FROM PostContent
        GROUP BY Subreddit_Name
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



##############################################################################################
##correlation between subreddit category of top posts and how many subscribers they have
## the subreddit category of the top posts of the days, against how many subscribers that category has  ##

def overlap_categories_listings():
    statement = '''
        SELECT DISTINCT Subreddit_Name, subreddit_subscribers
        FROM PostContent
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

    print(subreddit_label_lst)
    print(subreddit_subscriber_lst)



    ###how many of today's top posts fall under each of these subreddit categories
    top_post_subreddit_lst = []
    top_post_subreddit_value_lst = []

    statement = '''
        SELECT Subreddit_Name, count(*)
        FROM PostContent
        WHERE Subreddit_Name IN (
            SELECT DISTINCT Subreddit_Name
            FROM PostContent
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

    print(top_post_subreddit_lst)
    print(top_post_subreddit_value_lst)


    ##can also order by count


    # trace1 = go.Bar(
    #     x=subreddit_label_lst,
    #     y=subreddit_subscriber_lst,
    #     name='Most Subscribed Subreddits'
    # )
    # trace2 = go.Scatter(
    #     x=top_post_subreddit_lst,
    #     y=top_post_subreddit_value_lst,
    #     name="Subreddits Most Highly Represented in Today's top",
    #     yaxis="Number of listings"
    # )
    # data = [trace1, trace2]
    # layout = go.Layout(
    #     title="Most Subscribed Subreddits and Their Representation in Today's Top Listings",
    #     yaxis=dict(
    #         title='Subreddit Subscribers'

    #     ),
    #     yaxis2=dict(
    #         title="Number of today's top listings are from each given subreddit",
    #         titlefont=dict(
    #             color='rgb(148, 103, 189)'
    #         ),
    #         tickfont=dict(
    #             color='rgb(148, 103, 189)'
    #         ),
    #         overlaying='x',
    #         side='right'
    #     )
    # )
    # fig = go.Figure(data=data, layout=layout)
    # plot_url = py.plot(fig, filename='multiple-axes-double')




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

        # "anchor": 'free',
        # "position":0.85, 



##############################################################################################


### what percent of posts from each have original content or a video in bar chart
