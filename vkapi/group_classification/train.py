

def train(api, path):
    import pandas as pd
    df = pd.read_csv(path)
    group_ids = df['group_id'].values
    group_urls = df['group_id'].values
    labels = df['label'].values


if __name__ == '__main__':
    from .. import api as vkapi
    train(vkapi.get_api(), './train.csv')

