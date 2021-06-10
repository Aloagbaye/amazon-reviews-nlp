# Import dependencies
import pandas as pd
import re
import string
from sklearn.feature_extraction.text import CountVectorizer


def combine_reviews(file):
    dfa = pd.read_csv(file)
    dfa = dfa[['reviews', 'Product Links']]
    column_headers = ['reviews', 'products']
    dfa.columns = column_headers
    dff = dfa.groupby(['products'])
    dff = dff.first()
    return dff


# clean text
def clean_text(text):
    text = text.lower()
    text = re.sub('\[.*?\]', '', text)
    text = re.sub('[%s]' % re.escape(string.punctuation), '', text)
    text = re.sub('\w*\d\w*', '', text)
    text = re.sub('[0-9]', '', text)
    text = re.sub('[‘’“”…]', '', text)
    text = re.sub('\n', '', text)
    return text


def create_dtm(data):
    data_clean = pd.DataFrame(data.reviews.apply(clean_text))
    cv = CountVectorizer(stop_words='english')
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
    filename = 'amazonreviews.csv'
    df = combine_reviews(filename)
    dtm = create_dtm(df)
    dtm.to_pickle("dtm.pkl")