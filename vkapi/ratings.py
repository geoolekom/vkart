QUANTILE = 0.0
SECS = 7200
SEQUENCE = 50

def get_normed_likes(posts):
    pass


def set_ratings(posts):
    likes_count = 0.01
    for post in posts:
        likes_count += post['like_count']
    likes_count /= len(posts)
    for post in posts:
        post['rating'] = post['like_count'] / likes_count

def get_photos(file_name):
    return pickle.load(open(file_name, 'rb'))

def get_photo_rates(photos, expectations):
    exp_rates = [photo.likes / expectations[photo.second // SECS] for photo in photos]
    soft_avgs = [soft_avg(exp_rates[t:t+SEQUENCE]) for t in range(len(exp_rates)-SEQUENCE)]
    return [[photo, math.log(exp_rate / avg + 1) / math.log(2.0)]
            for photo, avg, exp_rate in
            zip(photos, soft_avgs, exp_rates)]

def soft_avg(likes):
    left_quantile = int(QUANTILE * len(likes))
    right_quantile = int((1 - QUANTILE) * len(likes))
    sorted_likes = sorted(likes)
    sorted_likes = sorted_likes[left_quantile:right_quantile]
    return sum(sorted_likes)/(len(sorted_likes) + 0.0)

def get_best_photos(photos, destination, top):
    photos = [photo for photo in photos if photo.likes]
    print('count of photos={}'.format(len(photos)))

    photos_div_t = defaultdict(list)
    for photo in photos:
        photos_div_t[photo.second // SECS].append(photo)

    avgs = [sum([photo.likes for photo in sub_photos]) / len(sub_photos) for sub_photos in photos_div_t.values()]
    norm_avgs = [len(avgs) * avg / sum(avgs) for avg in avgs]

    photo_rates = get_photo_rates(photos, norm_avgs)
    photo_rates.sort(key=lambda p_r: p_r[1], reverse=True)
    # for index, p_r in enumerate(photo_rates[0:top]):
        # img = io.imread(p_r[0].link)
        # io.imsave('{}/{}({}).png'.format(destination, index, p_r[1]), img)

    return photo_rates[:top]