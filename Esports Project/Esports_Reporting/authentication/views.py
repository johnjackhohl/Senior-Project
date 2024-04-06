from django.shortcuts import render, redirect
from django.contrib.auth.views import LoginView
from django.urls import reverse
from django.contrib.auth import logout 
from .forms import NewUserForm
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required

# Custom Login View
class CustomLoginView(LoginView):
	template_name = 'login/login.html'

	def get_success_url(self):
		# Redirect to the home page after login
		return reverse('home')
	
	def dispatch(self, request, *args, **kwargs):
		# Redirect to the home page if the user is already logged in
		if request.user.is_authenticated:
			return redirect('home')  # Redirect to a 'home' URL or another appropriate view
		return super().dispatch(request, *args, **kwargs)

# User Registration View
def register(request):
	"""Adds a new user to the database

	Args:
		request

	Returns:
		redirect: redirects back to the login page
	"""
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
	"""Renders the home page

	Args:
		request

	Returns:
		render: renders the home page
	"""
	return render(request, "home_page/home_page.html")

def logout_view(request):
	"""Logs the user out of the system

	Args:
		request

	Returns:
		render: generates the logout page
	"""
	logout(request)
	return render(request, "login/logout.html")

def delete_account(request):
	"""Deletes the user account

	Args:
		request

	Returns:
		render: generates the delete account page
	"""
	User = get_user_model()
	user = User.objects.get(username=request.user)
	user.delete()
	logout(request)
	return redirect('login')