from django.urls import path
from . import views

urlpatterns = [
        path('', views.RocheListView.as_view(), name='index'),
        path('<int:pk>/', views.RocheDetailView.as_view(), name='roche'),
        path('<str:slug>/', views.ProfileDetailView.as_view(), name='profile'),
        # submit
        ]
