########################################
# login/urls.py
########################################


from django.conf.urls import url

from . import views
import django.contrib.auth.views as authviews

# namespace='account'

urlpatterns = [
    url(r'^$', authviews.login),
    url(r'^register/$', views.register, name='register'), # {% url 'account:register' %}
    url(r'^register/success/$', views.register_success, name='register_success'), # {% url 'account:register_success' %}
    url(r'^login/$', authviews.login, name='login'),
    url(r'^logout/$', authviews.logout, {'next_page': '/'}, name='logout'),
]




