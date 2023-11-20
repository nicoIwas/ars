import praw
import pandas as pd
import operator
from prawcore.exceptions import Forbidden

# informação de login pra usar a api
reddit = praw.Reddit(
    client_id="X5VievD6zOr85BqP28ON0g", # personal use script v
    client_secret="eVfkbkX7kCnAAcvxJFCK7KVYKVJYrg", # secret
    user_agent="ars_scrapper", # script name
    username="broccoli_soccer",
    password="alexandrepato12?",
)

comments_and_posts = [] # vetor inicial que vai o título e conteúdo dos posts ou o conteúdo dos comentários

# def is_post(instancia):
#     try:
#         instancia = str(submission.body) # caso seja comentario
#         return False
#     except AttributeError:
#         instancia = str(submission.title) # caso seja comentario
#         return True
# def has_multimidia(instancia):
#     ####
#     return True
# def has_minimal_content(instancia):
#     ###
#     return True

def list_redditors(redditors_names):

    for submission in reddit.subreddit("brasil").top(time_filter="month"):
    # print(type(str(submission.author)))
      if not operator.contains(redditors_names, str(submission.author)):
          redditors_names.append(str(submission.author))

    return redditors_names

redditors_names = []
final_redditors_list = []

redditors_name = list_redditors(redditors_names)


print("Lista inicial de nomes que postaram recentemente no r/brasil: ")
print(len(redditors_names), ": ", redditors_names)

# pra cada nome na lista
# if submission.subreddit.display_name == "brasil":

def select_redditors(redditors_names, final_redditors_list):

        for redditor in redditors_names:

            try:
                count = 0
                reverse_count = 0
                total_count = 0
                for submission in reddit.redditor(redditor).new(limit=250):
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
                        if len(final_redditors_list)>=30: break
            except Forbidden:
                continue

        return final_redditors_list

final_redditors_list = select_redditors(redditors_names, final_redditors_list)

print("Lista final de usuários ativos no r/brasilivre: ")
print(len(final_redditors_list), ": ", final_redditors_list)


df = pd.DataFrame() # dataframe com os autores e o conteúdo dos posts


def create_dataset(final_redditors_list):

      for redditor in final_redditors_list:
        count = 0
        try:
            for submission in reddit.redditor(redditor).new(limit=250):
                try:
                    content = str(submission.body) # caso seja comentario
                    comments_and_posts.append(content)

                except AttributeError:
                    content = str(submission.title) # caso seja post
                    post_content = str(submission.selftext)
                    content = "Titulo = " + content + "\n Conteúdo = " + post_content
                    comments_and_posts.append(content)
                  
            if(len(comments_and_posts) == 250):
                df[redditor] = comments_and_posts
                print(df)
                count+=1
                if count == 25: break
            comments_and_posts.clear()
        except Forbidden: continue
    
      return df

df = create_dataset(final_redditors_list)

df.to_csv('brasil.csv', sep=',', index=False)
        # print(redditor, end = " [")
        # print("brasil = " + str(count), end =", ")
        # print("brasilivre = " + str(reverse_count), end="]\n")
    # except Forbidden:
        # continue
