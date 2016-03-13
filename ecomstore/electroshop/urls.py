from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$',views.product_list, name='product_list'),
    # url(r'^$',views.category_list, name='category_list'),
    url(r'^search/$', views.search_product, name='search_product'),
    url(r'^categories/(?P<slug>[\w\-]+)$', views.category_list, name='category_list'),
    url(r'^product_detail/(?P<slug>[\w\-]+)$',views.product_detail, name='product_detail'),
    url(r'^register/$',views.register, name='register'),
    url(r'^accounts/login/$',views.user_login, name='login'),
    url(r'^logout/$', views.user_logout, name='logout'),
    url(r'^profile/dashboard/$',views.dashboard, name='dashboard'),

]

