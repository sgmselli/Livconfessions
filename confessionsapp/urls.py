from django.urls import path
from . import views

app_name = 'confessionsapp'

urlpatterns=[
    path('', views.index, name='index'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.signin, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('settings/', views.settings_view, name='setting'),
    path('profile/<str:pk>', views.profile, name='profile'),
    path('upload/', views.upload, name='upload'),
    path('like/', views.like_post, name='like'),
    path('deletepost/', views.deletepost, name='deletpost'),
    path('deleteprofile/', views.deleteprofile, name='deleteprofile'),
    path('subject/<str:pk>', views.subject, name='subject'),
    path('sitemap/', views.sitemap, name='sitemap'),
    path('search/', views.search, name='search'),
    path('delete/', views.deleteconfirm, name='delete'),
    path('accounts/password_reset', views.password_reset , name='password_reset'),
    path('accounts/passwordreset/done', views.passwordresetdone , name='password_reset_done'),
    path('accounts/reset/<uidb64>/<token>', views.passwordresetconfirm , name='password_reset_confirm'),
    path('accounts/reset', views.passwordresetcomplete , name='password_reset_complete'),
    
]