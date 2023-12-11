import pandas

if __name__ == '__main__':
    transformed_version_brasil = pandas.read_csv('transformed_data/brasil0.csv')
    transformed_version_brasilivre = pandas.read_csv('transformed_data/brasil1.csv')
    transformed = [transformed_version_brasil, transformed_version_brasilivre]

    original_version_brasil = pandas.read_csv('data/brasil.csv')
    original_version_brasilivre = pandas.read_csv('data/brasilivre.csv')
    original = [original_version_brasil, original_version_brasilivre]

    brasil_timestamp = pandas.read_csv('data/time_stamp_brasil.csv')
    brasilivre_timestamp = pandas.read_csv('data/time_stamp_brasilivre.csv')

    brasil_sub = pandas.read_csv('data/brasil_sub.csv')
    brasilivre_sub = pandas.read_csv('data/brasilivre_sub.csv')

    dflist = [pandas.DataFrame(), pandas.DataFrame(), pandas.DataFrame(), pandas.DataFrame()]
    timelist = [brasil_timestamp, brasilivre_timestamp]
    subreddits = [brasil_sub, brasilivre_sub]
    
    nameoriginal = ['brasil_original.csv', 'brasilivre_original.csv']
    nametransformed = ['brasil_transformed.csv', 'brasilivre_transformed.csv']
    
    for t in transformed:
        del t['Unnamed: 0']

    nameunion = [nameoriginal, nametransformed]
    union = [original, transformed]
    
    for group, namegroup in zip(union, nameunion):
        for dataset, timestamps, subreddit, newdf, name in zip(group, timelist, subreddits, dflist, namegroup):
            comments = []
            for i in range(dataset.shape[0]):
                for j in range(dataset.shape[1]):
                    comments.append(dataset.iloc[i, j])
            newdf['submissions'] = comments

            timestamp = []
            for i in range(timestamps.shape[0]):
                for j in range(timestamps.shape[1]):
                    timestamp.append(timestamps.iloc[i, j])
            newdf['timestamp'] = timestamp

            sub = []
            for i in range(subreddit.shape[0]):
                for j in range(subreddit.shape[1]):
                    sub.append(subreddit.iloc[i, j])
            newdf['subreddit'] = sub

            if name in ['brasil_transformed.csv', 'brasilivre_transformed.csv']:
                newdf = newdf[newdf['submissions'] != '!NONE!']
            newdf.to_csv('betterdata/' + name, index=False)
            print('=====================\n' + name)
            print(newdf)
