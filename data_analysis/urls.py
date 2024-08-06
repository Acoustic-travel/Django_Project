from django.urls import path
from . import views

urlpatterns = [
    path('', views.upload_csv, name='upload_csv'),
    path('analyze/<str:filename>/', views.analyze_data, name='analyze_data'),
]