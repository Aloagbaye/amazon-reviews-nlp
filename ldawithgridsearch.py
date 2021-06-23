import numpy as np
import pandas as pd
from sklearn.decomposition import LatentDirichletAllocation
from sklearn.model_selection import GridSearchCV
from configparser import ConfigParser

config_object = ConfigParser()
config_object.read("config.ini")
LDA_params = config_object["LDA"]

# no of components
n1 = int(LDA_params["no_of_components_1"])
n2 = int(LDA_params["no_of_components_2"])
n3 = int(LDA_params["no_of_components_3"])

# Learning decay
d1 = float(LDA_params["learning_decay_1"])
d2 = float(LDA_params["learning_decay_2"])
d3 = float(LDA_params["learning_decay_3"])


def lda_grid_search(dtm, n_1, n_2, n_3, d_1, d_2, d_3):
    search_params = {'n_components': [n_1, n_2, n_3], 'learning_decay': [d_1, d_2, d_3]}  # Define Search Param
    lda = LatentDirichletAllocation()  # Initialize the Model
    model = GridSearchCV(lda, param_grid=search_params)  # Initialize Grid Search Class
    model.fit(dtm)  # Do the Grid Search
    return model


def dominant_topic(dtm, model):
    lda_output = model.best_estimator_.transform(dtm)
    topicnames = ["Topic" + str(i) for i in range(model.best_estimator_.n_components)]
    df = pd.DataFrame(np.round(lda_output, 2), columns=topicnames, index=dtm.index)
    dom_topic = np.argmax(df.values, axis=1)  # Get dominant topic for each document
    df['dominant_topic'] = dom_topic
    return df


def display_topics(model, feature_names, no_top_words):
    topic_dict = {}
    for topic_id, topic in enumerate(model.components_):
        topic_list = [feature_names[i] for i in topic.argsort()[:-no_top_words - 1:-1]]
        topic_dict[topic_id] = topic_list
    return topic_dict


def run_lda(dtm, links, no_of_top_words):
    results = lda_grid_search(dtm, n1, n2, n3, d1, d2, d3)
    features = dtm.columns
    df_dt = dominant_topic(dtm, results)
    topics_dict = display_topics(results.best_estimator_, features, no_of_top_words)
    df_dt['topic_words'] = df_dt['dominant_topic'].apply(lambda x: topics_dict.get(x))
    product_names = {'products': [link.split('/')[3] for link in links]}
    df_dt['products'] = pd.DataFrame.from_dict(product_names)['products']
    return df_dt[['products', 'dominant_topic', 'topic_words']].reset_index(drop=True)