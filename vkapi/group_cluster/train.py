from ..group_classification.train import make_corpus
from ..group_classification.feature import extract_text
from ..parameters import sleep_constant
from time import sleep
import os


def train(api, path):
    import pandas as pd
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.ensemble import GradientBoostingClassifier
    from sklearn.externals import joblib
    import umap
    import matplotlib.pyplot as plt
    df = pd.read_csv(path)
    group_ids = df['group_id'].values
    corpus = make_corpus(api, group_ids)
    vectorizer = TfidfVectorizer()
    X = vectorizer.fit_transform([corpus[group_id] for group_id in group_ids])
    joblib.dump(vectorizer, 'vectorizer.joblib')
    embedding = umap.UMAP().fit_transform(X)
    plt.scatter(embedding)
    plt.show()
    


if __name__ == '__main__':
    from .. import api as vkapi
    train(vkapi.get_api(), './groups.txt')

