import numpy as np
import pandas as pd
import re, nltk, spacy, gensim
# SKLearn
from sklearn.decomposition import LatentDirichletAllocation, TruncatedSVD
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.model_selection import GridSearchCV

dtm = pd.read_pickle("dtm_stop.pkl")


# Build LDA Model
def lda_grid_search(n1, n2, n3, d1, d2, d3):
    # Define Search Param
    search_params = {'n_components': [n1, n2, n3], 'learning_decay': [d1, d2, d3]}
    # Init the Model
    lda = LatentDirichletAllocation()
    # Init Grid Search Class
    model = GridSearchCV(lda, param_grid=search_params)
    # Do the Grid Search
    model.fit(dtm)
    # Model Parameters
    print("Best Model's Params: ", model.best_params_)
    # Log Likelihood Score
    print("Best Log Likelihood Score: ", model.best_score_)
    # Perplexity
    print("Model Perplexity: ", model.best_estimator_.perplexity(dtm))
    return model


def dominant_topic(model):
    # Create Document - Topic Matrix
    lda_output = model.best_estimator_.transform(dtm)
    # column names
    topicnames = ["Topic" + str(i) for i in range(model.best_estimator_.n_components)]
    # index names
    docnames = ["Doc" + str(i) for i in range(dtm.shape[0])]
    # Make the pandas dataframe
    df = pd.DataFrame(np.round(lda_output, 2), columns=topicnames, index=docnames)
    # Get dominant topic for each document
    dom_topic = np.argmax(df.values, axis=1)
    df['dominant_topic'] = dominant_topic
    return df_document_topic


# Styling
def color_red(val):
    color = 'red' if val > .1 else 'black'
    return 'color: {col}'.format(col=color)


def make_bold(val):
    weight = 700 if val > .1 else 400
    return 'font-weight: {weight}'.format(weight=weight)


result = lda_grid_search(3, 4, 5, 0.3, 0.5, 0.7)
df_document_topic = dominant_topic(result)
# Apply Style
df_document_topics = df_document_topic.head(15).style.applymap(color_red).applymap(make_bold)
