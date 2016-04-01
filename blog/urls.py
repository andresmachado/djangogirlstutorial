from django.conf.urls import include, url
from . import views

urlpatterns = [
    url(r'^$', views.post_list),
    url(r'^post/(?P<pk>[0-9]+)/$', views.post_detail),
    url(r'^post/new/$', views.post_new, name='post_new'),
    url(r'^post/(?P<pk>[0-9]+)/edit/$', views.post_edit, name='post_edit'),
    url(r'^login/$', views.login_user),
    url(r'^accounts/register/$', 'blog.views.register', name='register'),
    url(r'^accounts/register/complete/$', 'blog.views.registration_complete', name='registration_complete'),
]
