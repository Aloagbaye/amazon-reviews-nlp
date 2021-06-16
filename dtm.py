import pandas as pd
import re
import string
from sklearn.feature_extraction import text
from sklearn.feature_extraction.text import CountVectorizer
from nltk import word_tokenize, pos_tag


def combine_reviews(file):
    dfa = pd.read_csv(file)
    dfa = dfa[['reviews', 'Product Links']]
    column_headers = ['reviews', 'products']
    dfa.columns = column_headers
    dff = dfa.groupby(['products'])
    dff = dff.first()
    return dff


def nouns_adj(texts):
    is_noun_adj = lambda pos: pos[:2] == 'NN' or pos[:2] == 'JJ'
    tokenized = word_tokenize(texts)
    nouns_adje = [word for (word, pos) in pos_tag(tokenized) if is_noun_adj(pos)]
    return ' '.join(nouns_adje)


def nouns(texts):
    is_noun = lambda pos: pos[:2] == 'NN'
    tokenized = word_tokenize(texts)
    all_nouns = [word for (word, pos) in pos_tag(tokenized) if is_noun(pos)]
    return ' '.join(all_nouns)


def clean_text(texts):
    texts = texts.lower()
    texts = re.sub('\[.*?\]', '', texts)
    texts = re.sub('[%s]' % re.escape(string.punctuation), '', texts)
    texts = re.sub('\w*\d\w*', '', texts)
    texts = re.sub('[0-9]', '', texts)
    texts = re.sub('[‘’“”…]', '', texts)
    texts = re.sub('\n', '', texts)
    texts = nouns_adj(texts)
    return texts


def create_dtm(data):
    add_stop_words = ['like', 'im', 'know', 'just', 'dont', 'thats', 'right', 'people',
                      'youre', 'got', 'gonna', 'time', 'think', 'yeah', 'said']

    stop_words = text.ENGLISH_STOP_WORDS.union(add_stop_words)
    data_clean = pd.DataFrame(data.reviews.apply(clean_text))
    cv = CountVectorizer(stop_words=stop_words)
    data_cv = cv.fit_transform(data_clean.reviews)
    data_dtm = pd.DataFrame(data_cv.toarray(), columns=cv.get_feature_names())
    data_dtm.index = data_clean.index
    return data_dtm


def run_dtm():
    file = 'amazonreviews.csv'
    dfr = combine_reviews(file)
    dtm_file = create_dtm(dfr)
    dtm_file.to_pickle("dtm.pkl")


if __name__ == "__main__":
    run_dtm()
