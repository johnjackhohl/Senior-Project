from django.urls import path, include
from .views import *
from .views import CustomLoginView



urlpatterns = [
    path('login/', CustomLoginView.as_view(), name='login'),
    path('register/', register, name='register'),
    path('home/', home, name='home'),
    path('logout/', logout_view, name='logout'),
	path('deleteAccount/', delete_account, name='delete-account')
]
