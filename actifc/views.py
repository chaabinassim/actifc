from django.shortcuts import render,redirect
from django.contrib.auth.views import LogoutView,LoginView
from django.contrib.auth import login
from django.contrib.auth.forms import AuthenticationForm
from .forms import SignupForm

def home_view(request):
    return render(request, 'home.html')  


class CustomLogoutView(LogoutView):
    template_name = 'auth/logout.html'  


class CustomLoginView(LoginView):
    template_name = 'auth/login.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:  # Check if the user is already logged in
            return redirect('home')  # Redirect to the homepage or another page
        return super().dispatch(request, *args, **kwargs)



def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Automatically log in after sign-up
            return redirect('home')  # Redirect to a home page or dashboard
    else:
        form = SignupForm()
    return render(request, 'auth/signup.html', {'form': form})