import pandas as pd
import networkx as nx

sub_brasil = pd.read_csv('data/brasil_sub.csv')
print(sub_brasil)
unique_subs_in_brasil = set()  # Use a set to automatically keep unique values

for column in sub_brasil:
    for value in sub_brasil[column]:
        unique_subs_in_brasil.add(value) 

superior_columns = sub_brasil.columns[sub_brasil.ne('brasil').any()]
superior_columns = list(superior_columns)
print(superior_columns)

print('===================================================================================================================================================================================================')
sub_graphs = nx.Graph()
redditors_names = nx.Graph()
print(unique_subs_in_brasil)
sub_graphs.add_nodes_from(unique_subs_in_brasil)
redditors_names.add_nodes_from(superior_columns)
print(sub_graphs)
print(redditors_names)

####
# TODO: for each redditor, he will point to the subreddits that they submmit.
# so, each redditor will have an arrow to an subreddit, up to 250