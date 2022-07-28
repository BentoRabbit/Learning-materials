from django.conf.urls import url
from django.contrib import admin
from django.urls import path, include

from clinicaltrial import views

urlpatterns = [
    path('', views.index_view),
    # path(r'^admin/', admin.site.urls),
    # path('index/', views.index2_view),
    url(r'^bar/$', views.ChartView.as_view(), name='clinicaltrial'),
    path('show/',views.index3_view),
    path('register/',views.register),
    path('login/', views.login_view),
    path('data/',views.data_view),
    path('edit/',views.edit_view),
    path('bar_toolbox/',views.bar_view),
    path('pie_show/',views.pie_view),
    path('city/', views.city_view),
    path('phase/', views.phase_view),
    path('show_add/', views.add_show),
    path('show_edit/', views.edit_show),
    # path('test/',views.test_show),
    # path('search/',views.search_view),
]

