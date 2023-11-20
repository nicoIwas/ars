import praw
import pandas as pd
import operator
from prawcore.exceptions import Forbidden

# informação de login pra usar a api
reddit = praw.Reddit(
    client_id="zgV5t449XkcKiSbZ_Y-pTQ", # personal use script v
    client_secret="mmTAsvjLTgJpJMQnU7kIPZqxZemV8w", # secret
    user_agent="nicolas_scrapper", # script name
    username="nub3090",
    password="10Pqlazm2._", 
)

def get_submission(submission):
    try:
            content = str(submission.body) # caso seja comentario
            return content
    except Exception:
            content = str(submission.title) # caso seja post
            post_content = str(submission.selftext)
            content = "Titulo = " + content + "\n Conteúdo = " + post_content
            return content
    
def list_redditors(redditors_names):
    for submission in reddit.subreddit("brasil").top(time_filter="month"):
      if not operator.contains(redditors_names, str(submission.author)):
          redditors_names.append(str(submission.author))
    return redditors_names

def select_redditors(redditors_names, final_redditors_list, df):
    comments_and_posts = []
    for redditor in redditors_names:
        try:
            count = 0
            reverse_count = 0
            total_count = 0
            for submission in reddit.redditor(redditor).new(limit=250): 
                comments_and_posts.append(get_submission(submission=submission))
                if submission.subreddit.display_name == "brasil": 
                    total_count +=1
                    count+=1
                elif submission.subreddit.display_name == "brasilivre": 
                    reverse_count+=1
                    total_count+=1
                else: total_count+=1
            if count >= 75:
                print(redditor, " [brasil = ", count, ", brasilivre = ", reverse_count, ", total = ", total_count, "]")
                ratio = count/(count + reverse_count)
                if ratio >= 0.9 and total_count == 250:
                    print("Adicionando usuario ", redditor)
                    final_redditors_list.append(redditor)
                    df[redditor] = comments_and_posts
                    print(df)
                    if len(final_redditors_list)==25: 
                        print("tamanho máximo atingido, encerrando")
                        break
            comments_and_posts.clear()
        except Exception:
            continue
    return df

comments_and_posts = [] 
redditors_names = []
final_redditors_list = []
df = pd.DataFrame() 

redditors_names = list_redditors(redditors_names)
print("Lista inicial de nomes que postaram recentemente no r/brasil: ")
print(len(redditors_names), ": ", redditors_names)


df = select_redditors(redditors_names=redditors_names, final_redditors_list=final_redditors_list, df=df)
print("Lista final de usuários ativos no r/brasil: ")
print(len(final_redditors_list), ": ", final_redditors_list)
df.to_csv('brasil.csv', sep=',', index=False)
