import praw
import pandas as pd
import datetime as dt

reddit = praw.Reddit(client_id="",#my client id
                     client_secret="",  #your client secret
                     user_agent="my user agent", #user agent name
                     username = "",     # your reddit username
                     password = "")     # your reddit password

subreddit = reddit.subreddit('iPadPro')

#top_subreddit = subreddit.top(limit=10)
hot_subreddit = subreddit.hot(limit=10)

for submission in subreddit.hot(limit=1):
    print(submission.title, submission.id)

    topics_dict = { "title":[], 
                "score":[], 
                "id":[], "url":[],  
                "comms_num": [], 
                "created": [], 
                "body":[]}

for submission in hot_subreddit:
    topics_dict["title"].append(submission.title)
    topics_dict["score"].append(submission.score)
    topics_dict["id"].append(submission.id)
    topics_dict["url"].append(submission.url)
    topics_dict["comms_num"].append(submission.num_comments)
    topics_dict["created"].append(submission.created)
    topics_dict["body"].append(submission.selftext)

topics_data = pd.DataFrame(topics_dict)

topics_data.to_csv('test01.csv', index=False) 
