import time
import pandas as pd
from string import printable
import re
import demoji
import emoji
import wordninja
import langdetect
import nltk


def collect_data(filepath):
    return pd.read_csv(filepath)


def clean_emojis(text):
    emoji_remover = demoji.findall(text)
    for emoji in emoji_remover.keys():
        text = text.replace(emoji, '')
    return text

def clean_text(text, stop_words):
  text = str(text)
  text = text.lower()
  text = re.sub(r'#[A-Za-z0-9]*', ' ', text)
  text = re.sub(r'https*://.*', ' ', text)
  text = re.sub(r'@[A-Za-z0-9]+', ' ', text)
  text = re.sub(r'^.*:\n', '', text)
  tokens = nltk.tokenize.word_tokenize(text)
  text = ' '.join([w for w in tokens if not w.lower() in stop_words])
  text = re.sub(r'[%s]' % re.escape('!"#$%&\()*+,-./:;<=>?@[\\]^_`{|}~“…”’'), ' ', text)
  text = re.sub(r'\d+', ' ', text)
  text = re.sub(r'\s{2,}', ' ', text)
  text = text.replace('title', '').replace('selftext', '')
  return clean_emojis(text)
  

def clean_df(list_df):
    # in case its your first time running the script
    # nltk.download('stopwords')
    # nltk.download('punkt')
    stop_words = nltk.corpus.stopwords.words('portuguese')
    
    for df in list_df:
        for j in range(df.shape[1]):
            for i in range(df.shape[0]):
                df.iloc[i, j] = clean_text(df.iloc[i, j], stop_words)
    
    return list_df

    # while t:


if __name__ == '__main__':
    start = time.time()
    brazilian_subreddits = [collect_data('data/brasil.csv'), collect_data('data/brasilivre.csv')]
    elapsed = time.time()-start
    print('collected ' + str(elapsed))
    brazilian_subreddits = clean_df(brazilian_subreddits)
    elapsed = time.time()-start
    print('clean ' + str(elapsed))

    count = 0
    langdetect.DetectorFactory.seed = 0
    for clean_sub in brazilian_subreddits:
        for j in range(clean_sub.shape[1]):
            for i in range(clean_sub.shape[0]):
                try:
                    if langdetect.detect(clean_sub.iloc[i, j]) != 'pt':
                        print(clean_sub.iloc[i, j])
                        clean_sub.iloc[i, j] = '!NONE!'
                        print(clean_sub.iloc[i, j])
                        count += 1
                except langdetect.lang_detect_exception.LangDetectException:
                    clean_sub.iloc[i, j] = '!NONE!'
        elapsed = time.time()-start
        print('without language ' + str(elapsed))

    print(count)

    i = 0
    for full_portuguese_sub in brazilian_subreddits:   
        full_portuguese_sub.to_csv('transformed_data/brasil' + str(i) + '.csv')
        i+=1
    elapsed = time.time() - start
    print('saved files ' + str(elapsed))