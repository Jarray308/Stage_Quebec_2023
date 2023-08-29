from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('QUIZ.urls')),  # Remplacez 'QUIZ' par le nom de votre application
    # Autres URLs de votre projet...
]
