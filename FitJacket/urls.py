from django.contrib import admin
from django.urls import path, include

from workouts.urls import app_name


urlpatterns = [
    path('admin/', admin.site.urls, name='admin'),
    path('workouts/', include('workouts.urls'), name='workouts'),
    path('', include('home.urls'), name='home'),
    path('goals/', include('goals.urls'), name='goals'),
    path('accounts/', include(('accounts.urls', 'accounts'), namespace='accounts')),
    path('dashboard/', include('dashboard.urls'), name='dashboard'),
    path('social/', include('social.urls'), name='social'),

]
