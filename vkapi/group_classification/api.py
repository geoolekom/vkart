from .parameters import max_posts
from ..parameters import sleep_constant
from time import sleep


class GroupClassifier(object):
    vectorizer = None
    cls = None
    def __init__(self, api):
        from sklearn.externals import joblib
        if GroupClassifier.cls is None:
            GroupClassifier.cls = joblib.load('content_classifier.joblib')

        if GroupClassifier.vectorizer is None:
            GroupClassifier.vectorizer = joblib.load('vectorizer.joblib')
        
        self.api = api
        self.map_table = {
            0: 'nothing',
            1: 'picture',
            2: 'text',
        }

    def classify(self, group_id):
        from .feature import extract_text 
        while True:
            try:
                text = extract_text(self.api, group_id, max_posts=max_posts)
                break
            except Exception as e:
                print(e)
                sleep(2 * sleep_constant)
        res = GroupClassifier.cls.predict(GroupClassifier.vectorizer.transform([text]))[0]
        return res
    
    def classify_name(self, group_id):
        return self.map_table[self.classify(group_id)]


def classify_group(api, group_id):
    return GroupClassifier(api).classify(group_id)

