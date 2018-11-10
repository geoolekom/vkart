from django.db.models import signals
from django.dispatch import receiver

from accounts.models import User
from posts.tasks import update_best_posts


@receiver(signals.post_save, sender=User)
def update_posts_on_create(instance, created=False, **kwargs):
    if created:
        update_best_posts.delay(instance.id)
