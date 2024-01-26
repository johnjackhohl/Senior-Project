from django.urls import reverse
from django.shortcuts import redirect

class LoginRequiredMiddleware:
	def __init__(self, get_response):
		self.get_response = get_response

	def __call__(self, request):
		response = self.before_view(request)
		if response:
			return response
		response = self.get_response(request)
		response['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
		response['Pragma'] = 'no-cache'
		response['Expires'] = '0'
		return response

	def before_view(self, request):
		allowed_paths = [
			reverse('login'),
			reverse('register'),
			reverse('logout'),
			# Add other paths here if needed
		]

		if request.path not in allowed_paths and not request.user.is_authenticated:
			return redirect('login')
