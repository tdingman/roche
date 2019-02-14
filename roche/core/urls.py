from django.urls import path
from . import views

urlpatterns = [
        path('', views.RocheListView.as_view(), name='index'),
        path('submit/', views.RocheCreate.as_view(), name='submit'),
        path('<int:pk>/', views.RocheDetailView.as_view(), name='roche'),
        path('<int:pk>/join', views.join, name='join'),
        path('<int:pk>/accept', views.accept, name='accept'),
        path('<int:pk>/finalize', views.finalize, name='finalize'),
        path('<str:slug>/', views.ProfileDetailView.as_view(), name='profile'),
        ]
