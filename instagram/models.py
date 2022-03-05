from django.db import models
from accounts.models import Account
# Create your models here.

class Post(models.Model):
    user = models.ForeignKey(Account, on_delete=models.SET_NULL, null=True)
    image = models.ImageField()
    description = models.CharField(max_length=200)
    date_posted  =  models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.description


class Comment(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    message_body = models.CharField(max_length=100)
    date_posted = models.DateTimeField(auto_now_add=True)


    class Meta:
        verbose_name = 'comment'
        verbose_name_plural = 'comments'


    def __str__(self):
        return self.message_body

