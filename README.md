# reddit-post-database



Data sources used, including instructions for a user to access the data sources (e.g., API keys or client secrets needed, along with a pointer to instructions on how to obtain these and instructions for how to incorporate them into your program (e.g., secrets.py file format))
Any other information needed to run the program (e.g., pointer to getting started info for plotly)
Brief description of how your code is structured, including the names of significant data processing functions (just the 2-3 most important functions--not a complete list) and class definitions. If there are large data structures (e.g., lists, dictionaries) that you create to organize your data for presentation, briefly describe them.
Brief user guide, including how to run the program and how to choose presentation options.

Your GitHub repo must also contain a requirements.txt file that can be used by the teaching team to set up a virtual environment in which to run your project.


For this project I used Reddit.com API to obtain data about today's top posts, and their respective subreddits. I additionally scraped data from redditlist.com related to today's trending subreddits, and the like. 


#To use the program: 

##When you first create your database run:
create_reddit_db()

##Once a day to delete your cache, make a new cache dictionary, and get the day's data,:
load_cache(CACHE_FNAME)  
make_reddit_request(CACHE_FNAME)


##populate the table with today's data 
# lc = load_cache(CACHE_FNAME)
# populate_db_main_table()
# get_redditlist_info()

