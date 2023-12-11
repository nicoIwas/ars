import praw
import pandas as pd
import operator

reddit = praw.Reddit(
    client_id="zgV5t449XkcKiSbZ_Y-pTQ",
    client_secret="mmTAsvjLTgJpJMQnU7kIPZqxZemV8w",
    user_agent="nicolas_scrapper",
    username="nub3090",
    password="10Pqlazm2._",
)

def get_submission(submission):
    try:
        sub = str(submission.subreddit.display_name) + ' :\n'
        content = sub + str(submission.body)  # If it's a comment
        return content
    except Exception:
        sub = str(submission.subreddit.display_name) + ' :\n'
        content = str(submission.title)  # If it's a post
        post_content = str(submission.selftext)
        content = sub + "title : \n" + content + "\n selftext: \n" + post_content
        return content

def list_redditors(redditors_names):
    for submission in reddit.subreddit("brasilivre").top(time_filter="month"):
        if not operator.contains(redditors_names, str(submission.author)):
            redditors_names.append(str(submission.author))
    return redditors_names

def select_redditors(redditors_names, final_redditors_list, df, subreddit_tree, time_stamp):
    comments_and_posts = []
    sub_tree = []
    sub_ts = []
    for redditor in redditors_names:
        try:
            count = 0
            reverse_count = 0
            total_count = 0
            for submission in reddit.redditor(redditor).new(limit=250): 
                comments_and_posts.append(get_submission(submission=submission))
                sub_tree.append(submission.subreddit.display_name)
                sub_ts.append(submission.created_utc)
                if submission.subreddit.display_name == "brasilivre": 
                    total_count +=1
                    count+=1
                elif submission.subreddit.display_name == "brasil": 
                    reverse_count+=1
                    total_count+=1
                else: 
                    total_count+=1
            if count >= 75:
                print(redditor, " [brasilivre = ", count, ", brasil = ", reverse_count, ", total = ", total_count, "]")
                ratio = count/(count + reverse_count)
                if ratio >= 0.9 and total_count == 250:
                    print("Adicionando usuário ", redditor)
                    final_redditors_list.append(redditor)
                    df[redditor] = comments_and_posts
                    subreddit_tree[redditor] = sub_tree
                    time_stamp[redditor] = sub_ts
                    print(df)
                    if len(final_redditors_list)==25: 
                        print("Tamanho máximo atingido, encerrando")
                        break
            comments_and_posts.clear()
            sub_tree.clear()
            sub_ts.clear()
        except Exception:
            continue
    return df

comments_and_posts = [] 
redditors_names = []
final_redditors_list = []
df = pd.DataFrame() 
subreddit_tree = pd.DataFrame()
time_stamp = pd.DataFrame()
redditors_names = list_redditors(redditors_names=redditors_names)
print("Lista inicial de nomes que postaram recentemente no r/brasilivre: ")
print(len(redditors_names), ": ", redditors_names)


df = select_redditors(redditors_names=redditors_names, final_redditors_list=final_redditors_list, df=df,subreddit_tree=subreddit_tree, time_stamp=time_stamp)
print("Lista final de usuários ativos no r/brasilivre: ")
print(len(final_redditors_list), ": ", final_redditors_list)

df.to_csv('data/brasilivre.csv', sep=',', index=False)

subreddit_tree.to_csv('data/brasilivre_sub.csv', sep =',', index=False)
print(subreddit_tree)

time_stamp.to_csv('data/time_stamp_brasilivre.csv', sep = ',', index=False)
print(time_stamp)
