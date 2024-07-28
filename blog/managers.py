from django.db.models import Manager


class PostManager(Manager):
    def published(self, **kwargs):
        # return published posts
        return self.filter(
            status=self.model.Status.PUBLISHED,
            **kwargs,
        )
