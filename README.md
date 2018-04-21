# Final Reddit Database



Data sources used, including instructions for a user to access the data sources (e.g., API keys or client secrets needed, along with a pointer to instructions on how to obtain these and instructions for how to incorporate them into your program (e.g., secrets.py file format))
Any other information needed to run the program (e.g., pointer to getting started info for plotly)
Brief description of how your code is structured, including the names of significant data processing functions (just the 2-3 most important functions--not a complete list) and class definitions. If there are large data structures (e.g., lists, dictionaries) that you create to organize your data for presentation, briefly describe them.
Brief user guide, including how to run the program and how to choose presentation options.

Your GitHub repo must also contain a requirements.txt file that can be used by the teaching team to set up a virtual environment in which to run your project.


For this project I used Reddit.com API to obtain data about today's top posts, and their respective subreddits. I additionally scraped data from redditlist.com related to today's trending subreddits, and the like. The data from reddit.com makes up two tables in the database (PostContent and Subreddit_Table). They are joined by the key "Subreddit_Name_Prefixed". The scraped data from redditlist.com is compiled in three distinct tables (All_TimeRedditStats, Growing_RedditStats, TodayRedditStats).


# To use the program: 

### When you first create your database run:
create_reddit_db()
This function creates the structural database for all tables

### Once a day to delete your cache, make a new cache dictionary, and get the day's data and write them to the cache dictionary:
load_cache(CACHE_FNAME)  
make_reddit_request(CACHE_FNAME)
Upon calling make_reddit_request, it renews the users oauth tokens.


### To populate the tables with today's data: 
populate_db_main_table()
get_redditlist_info()
These functions take the data from the CACHE and populates the tables in the database

### To run the interactive program, which will prompt the user to select data visualization options:
interactive_prompt()
This function enables the user to select between four different viewing options from their terminal. All options will produce plot.ly visualizations (except "help" and "exit"). 

#### Note, this function is active in the file upon submission.


### Necessary secrets. 
The Reddit API requires the user sign up for a client_id and client_secret, along with the account username and password. 
The user should make a separate file called reddit_secrets, which they import at the top of the main file.
In the reddit_secrets file, their information should be entered as such:
client_secret = ""
client_id = ""
username = ""
password = ""

