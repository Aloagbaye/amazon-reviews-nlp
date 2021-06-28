import numpy as np
import pandas as pd
from sklearn.decomposition import LatentDirichletAllocation
from sklearn.model_selection import GridSearchCV


# Build LDA Model
def lda_grid_search(dtm, n1, n2, n3, d1, d2, d3):
    search_params = {'n_components': [n1, n2, n3], 'learning_decay': [d1, d2, d3]}  # Define Search Param
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


def run_lda(dtm, links, no_top_words):
    results = lda_grid_search(dtm, 5, 7, 10, 0.3, 0.5, 0.7)
    features = dtm.columns
    df_dt = dominant_topic(dtm, results)
    topics_dict = display_topics(results.best_estimator_, features, no_top_words)
    df_dt['topic_words'] = df_dt['dominant_topic'].apply(lambda x: topics_dict.get(x))
    product_names = {'products': [link.split('/')[1] for link in links]}
    df_dt['products'] = pd.DataFrame.from_dict(product_names)['products']
    return df_dt
