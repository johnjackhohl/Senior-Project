from django.shortcuts import render, redirect
from django.contrib.auth.views import LoginView
from django.urls import reverse
from django.contrib.auth import logout 
from .forms import NewUserForm

# Custom Login View
class CustomLoginView(LoginView):
	template_name = 'login/login.html'

	def get_success_url(self):
		# Redirect to the home page after login
		return reverse('home')
	
	def dispatch(self, request, *args, **kwargs):
		if request.user.is_authenticated:
			return redirect('home')  # Redirect to a 'home' URL or another appropriate view
		return super().dispatch(request, *args, **kwargs)

# User Registration View
def register(request):
	if request.method == "POST":
		form = NewUserForm(request.POST)
		if form.is_valid():
			form.save()
			return redirect('login')  # Redirect to the login page after successful registration
	else:
		form = NewUserForm()
	return render(request, "login/register.html", {"form": form})

# Home Page View
def home(request):
	return render(request, "home_page/home_page.html")

def logout_view(request):
	logout(request)
	return render(request, "login/logout.html")
