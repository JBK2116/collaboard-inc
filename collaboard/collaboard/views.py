from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from django.views.decorators.http import require_http_methods


@require_http_methods(["GET"])
def landing(request: HttpRequest) -> HttpResponse:
    if request.user.is_authenticated:
        return redirect("dashboard")
    return render(request=request, template_name="index.html", context={})


@login_required
@require_http_methods(["GET"])
def dashboard(request: HttpRequest) -> HttpResponse:
    return render(request=request, template_name="dashboard.html", context={})


@login_required
@require_http_methods(["GET", "POST"])
def account(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        request.user.delete()
        logout(request)
        return redirect("landing")
    else:
        return render(
            request=request,
            template_name="account.html",
            context={"account_deletion_failed": False},
        )
