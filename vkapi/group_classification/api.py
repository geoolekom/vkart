from .parameters import max_posts


class GroupClassifier(object):
    vectorizer = None
    cls = None
    def __init__(self, api):
        from sklearn.externals import joblib
        if GroupClassifier.vectorizer is None:
            GroupClassifier.vectorizer = joblib.load('content_claassifier.joblib')

        if GroupClassifier.cls is None:
            GroupClassifier.cls = joblib.load('vectorizer.joblib')
        
        self.api = api
        self.map_table = {
            0: 'nothing',
            1: 'picture',
            2: 'text',
        }

    def classify(self, group_id):
        from .feature import extract_text 
        text = extract_text(self.api, group_id, max_posts=max_posts)
        return GroupClassifier.cls.predict(GroupClassifier.vectorizer.predict([text]))[0]
    
    def classify_name(self, group_id):
        return self.map_table[self.classify(group_id)]


def classify_group(api, group_id):
    GroupClassifier(api).classify_name(group_id)

