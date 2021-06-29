import re
import string
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from nltk import word_tokenize, pos_tag


def combine_reviews(dfa):
    dfa = dfa[['products', 'reviews', ]]
    dfa['reviews'] = dfa.groupby(['products'])['reviews'].transform(lambda x: ' '.join(x))
    dfa = dfa.drop_duplicates()
    return dfa


def nouns_adj(texts, with_adj):
    if with_adj == "adjectives":
        tokenized = word_tokenize(texts)
        nouns_adje = [word for (word, pos) in pos_tag(tokenized) if lambda pos: pos[:2] == 'NN' or pos[:2] == 'JJ']
        return ' '.join(nouns_adje)
    else:
        tokenized = word_tokenize(texts)
        all_nouns = [word for (word, pos) in pos_tag(tokenized) if lambda pos: pos[:2] == 'NN']
        return ' '.join(all_nouns)


def clean_text(texts):
    texts = texts.lower()
    texts = re.sub('\[.*?\]', '', texts)
    texts = re.sub('[%s]' % re.escape(string.punctuation), '', texts)
    texts = re.sub('\w*\d\w*', '', texts)
    texts = re.sub('[0-9]', '', texts)
    texts = re.sub('[‘’“”…]', '', texts)
    texts = re.sub("[^A-Za-z]", ' ', texts)
    texts = re.sub('\n', '', texts)
    texts = nouns_adj(texts, "adjectives")
    return texts


def create_dtm(data):
    data_clean = pd.DataFrame(data.reviews.apply(clean_text))
    cv = CountVectorizer(stop_words='english')
    data_cv = cv.fit_transform(data_clean.reviews)
    data_dtm = pd.DataFrame(data_cv.toarray(), columns=cv.get_feature_names())
    data_dtm.index = data_clean.index
    return data_dtm


def run_dtm(dataframe):
    dfr = combine_reviews(dataframe)
    dtm_file = create_dtm(dfr)
    return dtm_file, dataframe.links
