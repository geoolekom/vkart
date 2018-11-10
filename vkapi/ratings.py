from collections import defaultdict
from math import sqrt
QUANTILE = 0.0
SECS = 7200
SEQUENCE = 50
DAY_SECS = 24 * 60 * 60

def get_normed_likes(posts):
    posts_div_t = defaultdict(list)
    for post in posts:
        posts_div_t[(post['timestamp'] % DAY_SECS) // SECS].append(post)
    posts_div_t = dict(posts_div_t)

    avgs = {k: sum([post['like_count'] for post in sub_posts]) / len(sub_posts) 
        for k, sub_posts in posts_div_t.items()}
   
    norm_avgs = {k : (1.0 + len(avgs) * avg / sum(avgs.values())) / 2.0 for k, avg in avgs.items()}

    return norm_avgs

def init_rates(posts, norm_avgs):
    for post in posts:
        post['rating'] = post['like_count'] / norm_avgs[(post['timestamp'] % DAY_SECS) // SECS]

def get_new_rates(posts, sequence_len):
    ratings = [post['rating'] for post in posts]
    new_rates = []
    for i in range(len(ratings)):
        l = max(0, i - sequence_len)
        r = min(len(posts) - 1, i + sequence_len)
        new_rates.append(sum(ratings[l : r]) / (len(ratings[l : r]) + 0.1))
    return new_rates

def set_ratings(posts):
    normed_likes = get_normed_likes(posts)
    init_rates(posts, normed_likes)
    sequence_len = int(sqrt(len(posts) + 1))
    new_rates = get_new_rates(posts, sequence_len)
    avg_rate = 0.0
    for post, new_rate in zip(posts, new_rates):
        post['rating'] /= new_rate
        avg_rate += post['rating']
    avg_rate /= len(posts)
    for post in posts:
        post['rating'] /= avg_rate


