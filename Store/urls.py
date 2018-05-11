
from django.urls import path

from . import views

app_name = 'store'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('create/', views.create, name='create'),
    path('api/', views.api, name='api'),
    path('<int:pk>/', views.DetailView.as_view(), name='detail'),
    path('<int:id>/update/', views.update, name='update'),
    path('<int:id>/cancel/', views.cancel, name='cancel'),
]


