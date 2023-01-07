from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib import messages
from django.shortcuts import render, redirect


def _login_views(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect("articles:list")
        return render(request, 'account/user404.html')
    return render(request, 'account/login.html')


def login_view(request, massages=None):
    if not request.user.is_anonymous:
        massages.info(request, "siz login qilib bolgansiz")
        return redirect("article:list")
    form = AuthenticationForm(request)
    if request.method == "POST":
        form =  AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            next_path = request.GET.get('next')
            messages.success(request, 'muvoffaqiyatli login qilidingiz!')
            if next_path:
                return redirect(next_path)
            return redirect('articles:list')
    return render(request, 'auth/login.html', {"form":form})


def logout_view(request):
    if not request.user.is_authenticated:
        return redirect('auth:login')
    if request.method == 'POST':
        logout(request)
        return redirect('auth:login')

    return render(request, 'auth/logout.html')


def register_view(request):
    if request.user.is_authenticated:
        return redirect("articles:list")
    form = UserCreationForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request, "Muvofaqiyatli royhatdan otingiz!")
        return redirect('auth:login')
    context = {
        'form': form
    }
    return render(request, "auth/register.html", context)

