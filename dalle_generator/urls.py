from django.urls import path
from . import views

app_name = 'dalle_generator'

urlpatterns = [
    path('generate-image/', views.generate_image, name='generate_image'),
]
