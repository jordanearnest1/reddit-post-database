import sqlite3 as sqlite3

import plotly.plotly as py
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




## To see the 10 most represented categories of subreddits in the "Top" results

statement = '''
    SELECT Subreddit_Name, count(*)
    FROM PostContent
    GROUP BY Subreddit_Name
    LIMIT 10
    '''

cur.execute(statement)    

results = cur.fetchall()

return_lst = []

label_lst = []
count_lst = []

for result in results:
    label_lst.append(result[0])
    count_lst.append(result[1])


print(label_lst)
print(count_lst)



labels = label_lst
values = count_lst
colors = ['#FEBFB3', '#E1396C', '#96D38C', '#D0F9B1', "#bfb3fe", '#feb3cd', "#b3f2fe", "#fd679b", "#fd81eb", "#b3cefe"]

trace = go.Pie(labels=labels, values=values,
               hoverinfo='label+value', textinfo='label', 
               textfont=dict(size=18),
               marker=dict(colors=colors, 
                           line=dict(color='#000000', width=2)))

py.plot([trace], filename='styled_pie_chart')


               # hoverinfo='label+value', textinfo='label', 
# 
