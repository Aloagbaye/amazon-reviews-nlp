# Import dependencies
import nltk
import pandas as pd
from nltk.stem import WordNetLemmatizer

nltk.download("wordnet")
lemmatizer = WordNetLemmatizer()
nltk.download("stopwords")
from nltk.corpus import stopwords

nltk.download("words")
from gensim.models import LdaModel  # To use the LDA model
import operator
import gensim
from gensim import corpora

df = pd.read_csv("amazonreviews.csv")
df_reviews = df.reviews
num_reviews = df_reviews.shape[0]
doc_set = [df_reviews[i] for i in range(num_reviews)]

# tokenizer for reg expressions
tokenizer = nltk.RegexpTokenizer(r'\w+')

# Define stop words
nltk_stpwd = stopwords.words('english')

# Stem words to get root words
sb_stemmer = nltk.SnowballStemmer('english')

texts = []

for doc in doc_set:
    tokens = tokenizer.tokenize(doc.lower())
    stopped_tokens = [token for token in tokens if not token in nltk_stpwd]
    stemmed_tokens = [sb_stemmer.stem(token) for token in stopped_tokens]
    texts.append(stemmed_tokens)  # Adds tokens to new list "texts"

texts_dict = corpora.Dictionary(texts)
texts_dict.save('reviews.dict')

print("IDs 1 through 10: {}".format(sorted(texts_dict.token2id.items(), key=operator.itemgetter(1), reverse=False)[:10]))

wordcheck = df_reviews.str.contains("price").value_counts()
ax = wordcheck.plot.bar(rot=0)

corpus = [texts_dict.doc2bow(text) for text in texts]
# Save a corpus to disk in the sparse coordinate Matrix Market format in a serialized format instead of random
corpora.MmCorpus.serialize('amazon_reviews.mm', corpus)

lda_model = gensim.models.LdaModel(corpus, alpha='auto', num_topics=3, id2word=texts_dict, passes=20)

lda_model.show_topics(num_topics=3, num_words=3)
