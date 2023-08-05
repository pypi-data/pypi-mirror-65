from django.db import models 


""" Category model managers. """
# Model Manager for ApptwoCategoryModel.
class CategoryModelSchemeQuerySet(models.QuerySet):

    def published(self):
        return self.filter(status='publish')

class CategoryModelSchemeManager(models.Manager):

    def get_queryset(self):
        return CategoryModelSchemeQuerySet(self.model, using=self._db)

    def published(self):
        return self.get_queryset().published()


""" Model manager for ApptwoArticleModel. """
# model manager start here.
class ArticleModelSchemeQuerySet(models.QuerySet):

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

class ArticleModelSchemeManager(models.Manager):

    def get_queryset(self):
        return ArticleModelSchemeQuerySet(self.model, using=self._db)

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
