
from django.urls import path

from . import views

app_name = 'warehouse'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('<int:id>/update/', views.update, name='update'),
    path('<int:pk>/', views.DetailView.as_view(), name='detail'),
    path('api/', views.api, name='api'),
]


