from posts.tasks import update_best_posts


def update_posts_on_create(user, is_new=False, *args, **kwargs):
    if is_new:
        update_best_posts.delay(user.id)
