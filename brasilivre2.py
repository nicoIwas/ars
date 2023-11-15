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

def is_post(instancia):
    try: 
        instancia = str(submission.body) # caso seja comentario
        return False
    except AttributeError:
        instancia = str(submission.title) # caso seja comentario
        return True
def has_multimidia(instancia):
    ####
    return True
def has_minimal_content(instancia):
    ###
    return True

redditors_names = []
redditors_already_chosen = ["uziel7","Silver_7777","haliax8802","BRTheDuality","Firehills","PrestigiousOkra4830","ILoveLeague","Holiday-Fly-7109","pete4180","DonaldLucas","greyoil","MajorMap9657","MacASM","BrunoofBrazil","AmbassadorUnusual250","OutrageousAd7829","Another_Johnny","EmploymentNo3326","Aria-shachou","weirnd201","evil-operationz","Southern_Copy_4128","tiovando","Di62028","TazFull","Puzzleheaded-Let-918","UhuMach","Junior_Judge6631","Feeling_Juggernaut64"]
final_redditors_list = []
for submission in reddit.subreddit("brasilivre").hot(limit=None):
    # print(type(str(submission.author)))
    if not operator.contains(redditors_names, str(submission.author)) and not operator.contains(redditors_already_chosen, str(submission.author)):
        redditors_names.append(str(submission.author))
# for submission in reddit.subreddit("brasilivre").new():
#     # print(type(str(submission.author)))
#     if not operator.contains(redditors_names, str(submission.author)) and not operator.contains(redditors_already_chosen, str(submission.author)):
#         redditors_names.append(str(submission.author))


print("Lista inicial de nomes que postaram recentemente no r/brasilivre: ")
print(redditors_names)

# pra cada nome na lista
# if submission.subreddit.display_name == "brasil":

for redditor in redditors_names:
    try:
        count = 0
        reverse_count = 0
        for submission in reddit.redditor(redditor).new(limit=300):
            if submission.subreddit.display_name == "brasilivre": count+=1
            elif submission.subreddit.display_name == "brasil": reverse_count+=1
        if count >= 75:
            print(redditor, " [brasil = ", reverse_count, ", brasilivre = ", count, "]") 
            ratio = count/(count + reverse_count)
            if ratio >= 0.9:
                print("adicionando usuario ", redditor)
                final_redditors_list.append(redditor)
                if len(final_redditors_list)>=16: break
    except Forbidden:
        continue

print("Lista final de usuários ativos no r/brasilivre: ")
print(final_redditors_list)
print("Tamanho da lista = ", len(final_redditors_list))
if len(final_redditors_list)<15: exit()

df = pd.DataFrame() # dataframe com os autores e o conteúdo dos posts
for redditor in final_redditors_list:
    count = 0
    try:
        for submission in reddit.redditor(redditor).new(limit=250):        
            try: 
                content = str(submission.body) # caso seja comentario
                comments_and_posts.append(content)
                # count+=1
            except AttributeError:
                content = str(submission.title) # caso seja post
                post_content = str(submission.selftext)
                content = "Titulo = " + content + "\n Conteúdo = " + post_content
                comments_and_posts.append(content)
                # count+=1
            # if count == 250: 
        if(len(comments_and_posts) == 250):
            df[redditor] = comments_and_posts
            print(df)
        comments_and_posts.clear()
                # break
    except Forbidden: continue
print(df)
df.to_csv('brasilivre2.csv', sep=',', index=False)
        # print(redditor, end = " [")
        # print("brasil = " + str(count), end =", ")
        # print("brasilivre = " + str(reverse_count), end="]\n")
    # except Forbidden:
        # continue