from django.contrib import admin
from django.urls import path, include
from . import views

app_name = 'webtoon'

urlpatterns = [
    path('', views.index, name='index'),
    path('<int:webtoon_id>/',views.detail, name='detail'),
    path('<int:webtoon_id>/review/', views.review, name='review'),
    path('<int:webtoon_id>/review_update/', views.review_update, name='review_update'),
    path('mypage/', views.mypage, name='mypage'),
    path('week/<str:webtoon_week>/', views.week, name='week'),
    path('search/', views.search, name='search'),
    path('aireco/', views.aireco, name='aireco'),
    path('test/', views.test, name='test'),

]
