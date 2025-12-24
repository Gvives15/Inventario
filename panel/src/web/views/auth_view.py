from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect, render
from django.views.decorators.http import require_http_methods


@require_http_methods(["GET"])
def login_page(request):
    if request.user.is_authenticated:
        return redirect("panel:dashboard")
    return render(request, "panel/login.html")


@require_http_methods(["POST"])
def login_submit(request):
    username = (request.POST.get("username") or "").strip()
    password = request.POST.get("password") or ""
    user = authenticate(request, username=username, password=password)
    if not user or not user.is_active:
        return render(request, "panel/login.html", {"error": "Credenciales inválidas"})
    login(request, user)
    return redirect("panel:dashboard")


@require_http_methods(["POST"])
def logout_submit(request):
    logout(request)
    return redirect("panel:login_page")
