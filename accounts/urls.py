from django.conf.urls import include, url 
from . import views



urlpatterns = [
   url(r'^login/$', views.login_view, name='user_login'),
   url(r'^logout/$', views.logout_view, name='user_logout'),
   #url(r'^user/list/$', views.user_list_view, name='user_list'),
   url(r'^user/list/$', views.UserListView.as_view(), name='user_list'),
]
