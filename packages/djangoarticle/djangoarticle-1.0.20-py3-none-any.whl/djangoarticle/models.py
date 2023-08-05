import random
from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.text import slugify
from django.contrib.contenttypes.models import ContentType
# Import from the local app.
from djangoarticle.managers import ArticleModelSchemeManager
from djangoarticle.managers import CategoryModelSchemeManager
# Import from the External app.
from taggit.managers import TaggableManager


""" Start category model here. """
# start model here.
class CategoryModelScheme(models.Model):

    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('publish', 'Publish'),
        ('withdraw', 'Withdraw'),
        ('private', 'Private')
    )

    serial        = models.IntegerField(blank=True, null=True)
    title         = models.CharField(max_length=35, unique=True, blank=False, null=False)
    slug          = models.SlugField(max_length=35, unique=True, blank=False, null=False)
    description   = models.TextField(blank=True, null=True)
    author        = models.ForeignKey(User, on_delete=models.CASCADE)
    status        = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    verification  = models.BooleanField(default=False)
    created_at    = models.DateTimeField(auto_now_add=True)
    updated_at    = models.DateTimeField(auto_now=True)

    # call all the model managers here.
    objects = CategoryModelSchemeManager()

    # invoke the str method here.
    def __str__(self):
        return self.title

    # overright the save method.
    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(CategoryModelScheme, self).save(*args, **kwargs)

    # get the absolute urls here.
    def get_absolute_url_for_category_detail_view(self):
        return reverse("djangoarticle:category_detail_view", kwargs={'category_slug': self.slug})

    def get_absolute_url_for_category_update_view(self):
        return reverse("djangoarticle:category_update_view", kwargs={'category_slug': self.slug})

    def get_absolute_url_for_category_delete_view(self):
        return reverse("djangoarticle:category_delete_view", kwargs={'category_slug': self.slug})

    # create the meta class.
    class Meta:
        ordering            = ['-pk']
        verbose_name        = 'Djangoarticle category'
        verbose_name_plural = 'Djangoarticle categories'


""" Start article model here. """
# start model here.
def image_upload_destination(instance, filename):
    if filename:
        get_extension = filename.split('.')[-1]
        get_filename = random.randint(0, 1000000000000)
        new_filename = f"IMG{get_filename}.{get_extension}"
        return(f'djangoarticle/{instance.author.id}_{instance.author.username}/{new_filename}')

class ArticleModelScheme(models.Model):

    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('publish', 'Publish'),
        ('withdraw', 'Withdraw'),
        ('private', 'Private')
    )

    serial         = models.IntegerField(blank=True, null=True)
    cover_image    = models.ImageField(null=True, blank=True, upload_to=image_upload_destination)
    title          = models.CharField(max_length=95, unique=True, blank=False, null=False)
    slug           = models.CharField(max_length=95, unique=True, blank=False, null=False)
    category       = models.ForeignKey(CategoryModelScheme, on_delete=models.CASCADE)
    description    = models.TextField(blank=True, null=True)
    shortlines     = models.TextField(blank=True, null=True)
    content        = models.TextField()
    author         = models.ForeignKey(User, on_delete=models.CASCADE)
    status         = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    verification   = models.BooleanField(default=False)
    is_promote     = models.BooleanField(default=False)
    is_trend       = models.BooleanField(default=False)
    is_promotional = models.BooleanField(default=False)
    total_views    = models.IntegerField(blank=True, null=True, default=0)
    created_at     = models.DateTimeField(auto_now_add=True)
    updated_at     = models.DateTimeField(auto_now=True)

    # call all the model manager here.
    objects = ArticleModelSchemeManager()
    tags    = TaggableManager(blank=True)

    # call the str method here.
    def __str__(self):
        return self.title

    # overright the save method.
    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(ArticleModelScheme, self).save(*args, **kwargs)

    # get absolute urls here.
    def get_absolute_url_for_article_detail_view(self):
        return reverse("djangoarticle:article_detail_view", kwargs={'article_slug': self.slug})

    def get_absolute_url_for_article_update_view(self):
        return reverse("djangoarticle:article_update_view", kwargs={'article_slug': self.slug})

    def get_absolute_url_for_article_delete_view(self):
        return reverse("djangoarticle:article_delete_view", kwargs={'article_slug': self.slug})

    def get_absolute_url_for_category_detail_view(self):
        return reverse("djangoarticle:category_detail_view", kwargs={'category_slug': self.category})

    def get_absolute_url_for_article_view(self, **kwargs):
        return reverse('djangoarticle:article_view', kwargs={'article_slug': self.slug})

    @property
    def get_for_model(self):
        instance = self
        return ContentType.objects.get_for_model(instance.__class__)

    # call the meta class.
    class Meta:
        ordering            = ['-pk']
        verbose_name        = 'Djangoarticle article'
        verbose_name_plural = 'Djangoarticle articles'
