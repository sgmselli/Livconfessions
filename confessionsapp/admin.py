from django.contrib import admin
from django.contrib.auth.models import Group

from .models import Profile, Post, LikePost, SubjectPage

admin.site.register(Profile)
admin.site.register(LikePost)
admin.site.register(Post)
admin.site.register(SubjectPage)

admin.site.unregister(Group)