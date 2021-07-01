import numpy as np
import pandas as pd
from sklearn.decomposition import LatentDirichletAllocation
from sklearn.model_selection import GridSearchCV
from configparser import ConfigParser

config_object = ConfigParser()
config_object.read("config.ini")
LDA_params = config_object["LDA"]

no_of_topics = int(LDA_params["no_of_components"])
max_iteration = int(LDA_params["max_iter"])


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
    results = LatentDirichletAllocation(n_topics=no_of_topics, max_iter=max_iteration).fit(dtm)
    features = dtm.columns
    df_dt = dominant_topic(dtm, results)
    topics_dict = display_topics(results, features, no_of_top_words)
    df_dt['topic_words'] = df_dt['dominant_topic'].apply(lambda x: topics_dict.get(x))
    product_names = {'products': [link.split('/')[3] for link in links]}
    df_dt['products'] = pd.DataFrame.from_dict(product_names)['products']
    return df_dt[['products', 'dominant_topic', 'topic_words']].reset_index(drop=True)