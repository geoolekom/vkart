from .feature import extract_text
from ..parameters import sleep_constant
from time import sleep
import os
from .parameters import max_posts


def train(api, path):
    import pandas as pd
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.ensemble import GradientBoostingClassifier
    from sklearn.externals import joblib
    df = pd.read_csv(path)
    group_ids = df['group_id'].values
    group_urls = df['group_id'].values
    labels = df['label'].values
    corpus = make_corpus(api, group_ids)
    vectorizer = TfidfVectorizer()
    X = vectorizer.fit_transform([corpus[group_id] for group_id in group_ids])
    cls = GradientBoostingClassifier() 
    cls.fit(X, labels)
    joblib.dump(clf, 'content_classifier.joblib') 
    joblib.dump(vectorizer, 'vectorizer.joblib') 


def make_corpus(api, group_ids):
    from tqdm import tqdm
    import pickle
    corpus = {}
    if os.path.exists('corpus.pkl'):
        with open('corpus.pkl', 'rb') as f:
            corpus = pickle.load(f)

    for group_id in tqdm(group_ids):
        if group_id in corpus:
            continue
        sleep_constant_cur = sleep_constant
        while True:
            sleep(sleep_constant_cur)
            try:
                corpus[group_id] = extract_text(api, str(group_id), max_posts=max_posts)
                break
            except:
                sleep_constant_cur *= 2
        with open('corpus.pkl', 'wb') as f:
            pickle.dump(corpus, f)
    return corpus


if __name__ == '__main__':
    from .. import api as vkapi
    train(vkapi.get_api(), './train.csv')

