import praw
reddit = praw.Reddit(user_agent='Mozilla/5.0',client_id='6YKv7QY_LYtgqL6x0VKgRw',client_secret='999dPOb7VY_4cW3-k0ilIjY11IMYxA',username='****',password='*****')

url ="https://www.reddit.com/r/PremierLeague/comments/1b3plxw/liverpool_man_city_arsenal_who_will_win_the_2324/"

post1 = reddit.submission(url=url)

print(post1.selftext)
