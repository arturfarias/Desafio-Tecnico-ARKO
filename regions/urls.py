from django.urls import path
from . import views

urlpatterns = [
    path('', views.state, name='states'),
    path('municipalities/', views.municipalities, name='municipalities'),
    path('districts/', views.districts, name='districts'),
]