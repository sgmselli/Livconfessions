from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.middleware.csrf import get_token
from django.views.generic import ListView
import json

from .models import Profile, Post, LikePost, SubjectPage


@login_required(login_url='/login/')
def index(request):
    user_object = User.objects.get(username=request.user.username)
    user_profile = Profile.objects.get(user=user_object)

    userpost = request.user.username

    posts = Post.objects.all()

    
    post_id= request.GET.get('postid')
    print(post_id)
    like_filter = LikePost.objects.filter(post_id=post_id, username=userpost).first()

    context = {'user_profile':user_profile, 
    
    'userpost':userpost, 
    'posts':posts,
    'page':' Home',
    }

    return render(request, 'confessionsapp/index.html', context)

def signup(request):

    user = request.user.username

    if request.method == 'POST':
        firstname = request.POST['firstname']
        lastname = request.POST['lastname']
        username = request.POST['username']
        email = request.POST['email']
        uni = request.POST['uni']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        
        
        if password1 == password2:
            if User.objects.filter(email=email).exists():
                messages.info(request, 'Email taken')
                return redirect('/signup/')
            if User.objects.filter(username=username).exists():
                messages.info(request, 'Username taken')
                return redirect('/signup/')
            else:
                user = User.objects.create_user(first_name=firstname, last_name=lastname, username=username, email=email, password=password1)
                user.save()
                
                #log user in
                user_login = authenticate(username=username, password=password1)
                login(request, user_login)

                #create profile object for user
                user_model = User.objects.get(username=username)
                new_profile = Profile.objects.create(user=user, id_user=user_model.id, firstname=firstname, lastname=lastname, email=email, uni=uni)
                new_profile.save()
                return redirect('/login/') 
        else:
            messages.info (request, 'Passwords did not match')
            return redirect('/signup/')
    
    return render(request, 'registration/signup.html', {'user':user, 'page':'Sign up'})

def signin(request):
    user = request.user.username

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password1']

        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('/')
        else:
            messages.info(request, 'Username or password details were not correct')
            return redirect('/login/')
    else:
        return render(request, 'registration/login.html', {'user':user, 'page':'Sign in'})

@login_required(login_url=('/login/'))
def logout_view(request):
    logout(request)
    return redirect('/login/')

@login_required(login_url=('/login/'))
def settings_view(request):
    user_profile = Profile.objects.get(user=request.user)

    if request.method == 'POST':
        if request.FILES.get('image') == None:
            image = user_profile.profileimg
            firstname = request.POST['firstname']
            lastname = request.POST['lastname']
            email = request.POST['email']

            user_profile.profileimg = image
            user_profile.firstname = firstname
            user_profile.lastname = lastname
            user_profile.email = email
            user_profile.save()

        if request.FILES.get('image') != None:
            image = request.FILES.get('image')
            firstname = request.POST['firstname']
            lastname = request.POST['lastname']
            email = request.POST['email']

            user_profile.profileimg = image
            user_profile.firstname = firstname
            user_profile.lastname = lastname
            
            user_profile.save()
        
        return redirect('/settings/')

    else:
        return render(request, 'confessionsapp/settings.html', {'user_profile':user_profile, 'page':'Settings'})

@login_required(login_url=('/login/'))
def upload(request):
    user_object = User.objects.get(username=request.user.username)
    user_profile = Profile.objects.get(user=user_object)

    subjectselect = SubjectPage.objects.all()

    if request.method == 'POST':
        user = request.user.username

        confession = request.POST['confession']
        subject = request.POST['subject']
        privacy = request.POST['privacy']
        user_post = Post.objects.create(user=user, confession=confession, subject=subject, privacy=privacy)
        user_post.save()
        return redirect('/')
    else:
        return render(request, 'confessionsapp/upload.html',  {'user_profile':user_profile, 'subjectselect':subjectselect, 'page':'Confess'})

@login_required(login_url='/login/')
def deletepost(request):
    post_id = request.GET.get('post_id')
    post = Post.objects.get(id=post_id)
    post.delete()

    return redirect('/')

@login_required(login_url='/login/')
def deleteprofile(request):
    user_object = User.objects.get(username=request.user.username)
    user_object.delete()

    return redirect('/login/')

@login_required(login_url='/login/')
def deleteconfirm(request):
    user_object = User.objects.get(username=request.user.username)
    user_profile = Profile.objects.get(user=user_object)

    return render(request, 'confessionsapp/deleteuser.html', {'user_profile':user_profile, 'page':'Delete'})


@login_required(login_url='/login/')
def like_post(request):
    username = request.user.username

    
    if request.POST.get('action') == 'post':
        get_token(request)
        result=''
        post_id= request.POST.get('postid')
        post = Post.objects.get(id=post_id)
        like_filter = LikePost.objects.filter(post_id=post_id, username=username).first()
    
        if like_filter == None:

            heart = '<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="red" class="bi bi-heart-fill" viewBox="0 0 16 16"><path fill-rule="evenodd" d="M8 1.314C12.438-3.248 23.534 4.735 8 15-7.534 4.736 3.562-3.248 8 1.314z"/></svg>'

            new_like = LikePost.objects.create(post_id=post_id, username=username)
            new_like.save()
            post.likes += 1
            result = post.likes
            post.save()
            
        
        else:
            heart = '<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="red" class="bi bi-heart" viewBox="0 0 16 16"><path d="m8 2.748-.717-.737C5.6.281 2.514.878 1.4 3.053c-.523 1.023-.641 2.5.314 4.385.92 1.815 2.834 3.989 6.286 6.357 3.452-2.368 5.365-4.542 6.286-6.357.955-1.886.838-3.362.314-4.385C13.486.878 10.4.28 8.717 2.01L8 2.748zM8 15C-7.333 4.868 3.279-3.04 7.824 1.143c.06.055.119.112.176.171a3.12 3.12 0 0 1 .176-.17C12.72-3.042 23.333 4.867 8 15z" /></svg>'


            like_filter.delete()
            post.likes -= 1
            result = post.likes
            post.save()
        
        return JsonResponse({'result':result, 'heart':heart})
    
@login_required(login_url='/login/')
def profile(request, pk):
    user_object = User.objects.get(username=pk)
    user_profile = Profile.objects.get(user=user_object)
    user_posts = Post.objects.filter(user=pk)
    post_amount = len(user_posts)

    context = {
        'user_object' : user_object,
        'user_profile' : user_profile,
        'user_posts' : user_posts,
        'post_amount' : post_amount,
        'page':'@'+str(user_profile.user),
    }
    return render(request, 'confessionsapp/profile.html', context)

@login_required(login_url='/login/')
def subject(request, pk):
    user_object = User.objects.get(username=request.user.username)
    user_profile = Profile.objects.get(user=user_object)

    subjectpage = SubjectPage.objects.get(subject=pk)
    posts = Post.objects.all()
    

    context = {
        'user_object':user_object,
        'user_profile':user_profile,
        'posts':posts,
        'page':subjectpage,
        'pk':pk,
    }
    

    return render(request, 'confessionsapp/subject.html', context)

@login_required(login_url='/login/')
def sitemap(request):
    user_object = User.objects.get(username=request.user.username)
    user_profile = Profile.objects.get(user=user_object)

    context = {
        'user_object':user_object,
        'user_profile':user_profile,
        'page':'Sitemap'
    }

    return render(request, 'confessionsapp/subjectmap.html', context)

@login_required(login_url='/login/')
def search(request):

    user_object = User.objects.get(username=request.user.username)
    user_profile = Profile.objects.get(user=user_object)
    profiles = Profile.objects.all()    
     

    context = {
        'user_object':user_object,
        'user_profile':user_profile,
        'page':'Search',
        'profiles':profiles,
    }
    return render(request, 'confessionsapp/search.html', context)

@login_required(login_url='/login/')
def password_reset(request):
    return render(request, 'registration/password_reset_form.html')

@login_required(login_url='/login/')
def passwordresetdone(request):
    return render(request, 'registration/password_reset_done.html')

@login_required(login_url='/login/')
def passwordresetconfirm(request):
    return render(request, 'registration/password_reset_confirm.html')

@login_required(login_url='/login/')
def passwordresetcomplete(request):
    return render(request, 'registration/password_reset_complete.html')


