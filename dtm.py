# Import dependencies
import pandas as pd
import re
import string
from sklearn.feature_extraction.text import CountVectorizer

df = pd.read_csv("amazonreviews.csv")
df_reviews = df.reviews
num_reviews = df_reviews.shape[0]
doc_set = [df_reviews[i] for i in range(num_reviews)]

df = df[['reviews', 'Product Links']]
column_headers = ['reviews', 'products']
df.columns = column_headers
dff = df.groupby(['products'])
dff = dff.first()


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


cleandata = lambda x: clean_text(x)
data_clean = pd.DataFrame(dff.reviews.apply(cleandata))

cv = CountVectorizer(stop_words='english')
data_cv = cv.fit_transform(data_clean.reviews)
data_dtm = pd.DataFrame(data_cv.toarray(), columns=cv.get_feature_names())
data_dtm.index = data_clean.index
