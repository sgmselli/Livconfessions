from django.db import models
from django.contrib.auth import get_user_model
import uuid #generates unique id
from datetime import datetime

User = get_user_model()

class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    id_user = models.IntegerField()
    profileimg = models.ImageField(upload_to='profile_images', default='default-profile-picture.jpg')
    firstname = models.CharField(max_length=100, blank=True)
    lastname = models.CharField(max_length=100, blank=True)
    email = models.CharField(max_length=100, blank=True)
    uni = models.CharField(max_length=70, blank=True)

    def __str__(self):
        return self.user.username

class Post(models.Model):
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    user = models.CharField(max_length=80)
    confession = models.CharField(max_length=300, editable = False)
    created_at = models.DateTimeField(default=datetime.now)
    likes = models.IntegerField(default=0)
    subject = models.CharField(max_length=40, default="general")
    privacy = models.CharField(max_length=10, default='show')


    def __str__(self):
        return self.user 

class LikePost(models.Model):
    post_id = models.CharField(max_length=500)
    username = models.CharField(max_length=100)

    def __str__(self):
        return self.username

class SubjectPage(models.Model):
    title = models.CharField(max_length=40, default='General')
    subject = models.CharField(max_length=40, default='general')

    def __str__(self):
        return self.title