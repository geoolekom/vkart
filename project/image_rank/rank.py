

class Ranker:
    model = None
    def __init__(self):
        from keras.models import Model
        from keras.layers import Dense, Dropout
        from keras.applications.inception_resnet_v2 import InceptionResNetV2
        from keras.applications.inception_resnet_v2 import preprocess_input
        from keras.preprocessing.image import load_img, img_to_array
        import tensorflow as tf
        from .nima_utils.score_utils import mean_score, std_score

        from django.conf import settings
        if Ranker.model is None:
            with tf.device('/CPU:0'):
                base_model = InceptionResNetV2(input_shape=(None, None, 3), include_top=False, pooling='avg', weights=None)
                x = Dropout(0.75)(base_model.output)
                x = Dense(10, activation='softmax')(x)
                try:
                    weights_path = settings.IMAGE_RANK_WEIGHTS_PATH
                except:
                    import logging
                    logging.fatal("YOU MUST SPECIFY FUNCKING WEIGHTS PATH")
                    return
                model = Model(base_model.input, x)
                model.load_weights(weights_path)
            Ranker.model = model

    def get_mean_std_scores(self, images):
        if Ranker.model is None:
            return [{'mean': 0, 'std': 0}] * len(images)
        from .nima_utils.score_utils import mean_score, std_score
        from keras.applications.inception_resnet_v2 import preprocess_input
        import numpy as np
        res = []
        for image in images:
            image = np.expand_dims(image, axis=0)
            image = preprocess_input(image)
            scores = Ranker.model.predict(image)
            mean = mean_score(scores)
            std = std_score(scores)
            res.append({'mean': mean, 'std': std})
        return res


def rank_images(images):
    return Ranker().get_mean_std_scores(images)


def rank_urls(urls):
    import requests
    from io import BytesIO
    from keras.preprocessing.image import load_img, img_to_array
    from PIL import Image
    images = []
    for url in urls:
        x = Image.open(BytesIO(requests.get(url, stream=True).content))
        x = x.resize((224, 224))
        x = img_to_array(x)
        images.append(x)
    return Ranker().get_mean_std_scores(images)


def rank_paths(paths):
    from keras.preprocessing.image import load_img, img_to_array
    from PIL import Image
    images = []
    for path in paths:
        x = load_img(path)
        x = x.resize((224, 224))
        x = img_to_array(x)
        images.append(x)
    return Ranker().get_mean_std_scores(images)

