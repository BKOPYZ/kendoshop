from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.conf import settings

User = settings.AUTH_USER_MODEL


def register_view(request):
    context = dict()
    if request.method == "POST" and request.POST.get("submit", False):
        post = request.POST
        first_name = post.get("firstname", None)
        last_name = post.get("lastname", None)
        user_profile = post.get("user_profile", None)
        username = post.get("username")
        email = post.get("email")
        password = post.get("password")
        confirm_password = post.get("confirm_password")

        context["username"] = username
        context["email"] = email
        context["userprofile"] = user_profile

        # error_message = ""
        is_valid = True

        if User.objects.filter(username=username).exists():
            messages.error("error exists username")
            is_valid = False

        if password != confirm_password:
            messages.error("error password not the same")
            is_valid = False

        if is_valid:
            try:
                new_user = User.objects.create(
                    user_profile=user_profile,
                    username=username,
                    email=email,
                    first_name=first_name,
                    last_name=last_name,
                )
                new_user.set_password(password)
                new_user.save()
                messages.info(request, "Thanks for registering. You are now logged in.")
                new_user = authenticate(
                    username=email,
                    password=password,
                )
                login(request, new_user)
                return redirect("core:home")
            except Exception as e:
                messages.error(request, e)
    return render(request, "userauths/sign-up.html", context)


def login_view(request):
    if request.user.is_authenticated:
        return redirect("core:home")

    context = dict()
    if request.method == "POST":
        post = request.POST
        email = post.get("email")
        password = post.get("password")

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExists:
            messages.error(request, "email does not exist")
        else:
            user = authenticate(request, email=email, password=password)

            if user is not None:

                login(request, user)
                messages.success(request, "you are login")
                return redirect("core:home")
            else:
                messages.error(
                    request, "user doesnot exist or password does not correct"
                )

    return render(request, "userauths/login.html", context)


def logout_view(request):
    logout(request)
    messages.success("You have logout")
    return redirect("userauths:login")
