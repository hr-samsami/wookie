from django.urls import path
from . import views

urlpatterns = [
    path('', views.RendererView.as_view())
]
