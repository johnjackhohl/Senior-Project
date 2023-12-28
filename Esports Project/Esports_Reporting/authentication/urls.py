from django.urls import path, include
from .views import CustomLoginView, register, home, logout


urlpatterns = [
    path('Overwatch/', include(('OverWatch_2.urls', 'OverWatch_2'), namespace='OverWatch_2')),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('register/', register, name='register'),
    path('home/', home, name='home'),
    path('logout/', logout, name='logout'),
]
