from django.db import models
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
from django.db.models.signals import pre_save, post_save
from .utils import slugify_instance_title
from django.utils import text
from django.urls import reverse
# Create your models here.

class Blog(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='post_author')
    blog_title = models.CharField(max_length=264, verbose_name='Put a Title')
    slug = models.SlugField(max_length=264, unique=True, blank=True, null=True, allow_unicode=True)
   #slug = models.SlugField(max_length=264,  unique=True)
    blog_content = models.TextField(verbose_name='Whats on your mind?')
    blog_image = models.ImageField(upload_to='blog_images', verbose_name='Image')
    publish_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-publish_date']
   
    def __str__(self):
        return self.blog_title

    #def get_absolute_url(self):
        # return f'/articles/{self.slug}/'
    #    return reverse("articles:detail", kwargs={"slug": self.slug})
    
    """
    def save(self, *args, **kwargs):
        # obj = Article.objects.get(id=1)
        # set something
        if self.slug is None:
            self.slug = slugify(self.blog_title)
        # if self.slug is None:
        #     slugify_instance_title(self, save=False)
        super().save(*args, **kwargs)
        # obj.save()
        # do another something
    """
    
def article_pre_save(sender, instance, *args, **kwargs):
    # print('pre_save')
    if instance.slug is None:
        slugify_instance_title(instance, save=False)
        #instance.slug = slugify(instance.blog_title)

pre_save.connect(article_pre_save, sender=Blog)

def article_post_save(sender, instance, created, *args, **kwargs):
    # print('post_save')
    if created:
        slugify_instance_title(instance, save=True)
        #instance.slug = slugify(instance.blog_title)
        #instance.save()
        
post_save.connect(article_post_save, sender=Blog)

class Comment(models.Model):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name='blog_comment')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_name')
    comment = models.TextField()
    comment_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-comment_date']

    def __str__(self):
        return self.comment

class Likes(models.Model):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name="liked_blog")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='liker_user')

    def __str__(self):
        return self.user + " likes " + self.blog
    