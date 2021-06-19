import numpy as np
import pandas as pd

from sklearn.decomposition import LatentDirichletAllocation
from sklearn.model_selection import GridSearchCV


# Build LDA Model
def lda_grid_search(dtm, n1, n2, n3, d1, d2, d3):
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


def dominant_topic(dtm, model):
    # Create Document - Topic Matrix
    lda_output = model.best_estimator_.transform(dtm)
    # column names
    topicnames = ["Topic" + str(i) for i in range(model.best_estimator_.n_components)]
    df = pd.DataFrame(np.round(lda_output, 2), columns=topicnames, index=dtm.index)
    # Get dominant topic for each document
    dom_topic = np.argmax(df.values, axis=1)
    df['dominant_topic'] = dom_topic
    return df


def display_topics(model, feature_names, no_top_words):
    topic_dict = {}
    for topic_id, topic in enumerate(model.components_):
        topic_list = [feature_names[i] for i in topic.argsort()[:-no_top_words - 1:-1]]
        topic_dict[topic_id] = topic_list
    return topic_dict


# Styling
def color_red(val):
    color = 'red' if val > .1 else 'black'
    return 'color: {col}'.format(col=color)


def make_bold(val):
    weight = 700 if val > .1 else 400
    return 'font-weight: {weight}'.format(weight=weight)


def run_lda(dtm, no_top_words):
    results = lda_grid_search(dtm, 5, 7, 10, 0.3, 0.5, 0.7)
    features = dtm.columns
    df_dt = dominant_topic(dtm, results)
    topics_dict = display_topics(results.best_estimator_, features, no_top_words)
    df_dt['topic_words'] = df_dt['dominant_topic'].apply(lambda x: topics_dict.get(x))
    # df_dt['dominant_topic']
    # Apply Style
    # df_dts = df_dt.style.applymap(color_red).applymap(make_bold)
    df_dt.to_csv("dominanttopics_adj_5_5.csv")



if __name__ == "__main__":
    dtmx = pd.read_pickle("dtm.pkl")
    run_lda(dtmx, 5)