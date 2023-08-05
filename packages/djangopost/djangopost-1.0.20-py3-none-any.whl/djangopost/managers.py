from django.db import models


""" Model Manager """
# Model Manager for ApptwoCategoryModel.
class CategoryModelQuerySet(models.QuerySet):

    def published(self):
        return self.filter(status='publish')

class CategoryModelManager(models.Manager):

    def get_queryset(self):
        return CategoryModelQuerySet(self.model, using=self._db)

    def published(self):
        return self.get_queryset().published()


""" Model manager for ArticleModel. """
# model manager here.
class ArticleModelQuerySet(models.QuerySet):
    
    def published(self):
        return self.filter(status='publish')

    def promoted(self):
        return self.published().filter(is_promote=True)

    def trending(self):
        return self.published().filter(is_trend=True)

    def author(self, username):
        return self.published().filter(author__username=username)

    def promotional(self):
        return self.published().filter(is_promotional=True, verification=True)

class ArticleModelManager(models.Manager):

    def get_queryset(self):
        return ArticleModelQuerySet(self.model, using=self._db)

    def published(self):
        return self.get_queryset().published()

    def promoted(self):
        return self.get_queryset().promoted()

    def trending(self):
        return self.get_queryset().trending()

    def author(self, username):
        return self.get_queryset().author(username)

    def promotional(self):
        return self.get_queryset().promotional()
