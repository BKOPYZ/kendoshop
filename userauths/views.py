from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib import messages
from userauths.models import User


def register_view(request):
    context = dict()
    if request.method == "POST" and (post := request.POST.get("submit", False)):

        user_profile = post.get("user_profile", None)
        username = post.get("username")
        email = post.get("email")
        password = post.get("password")
        confirm_password = post.get("confirm_password")

        # error_message = ""
        is_valid = True

        if User.objects.filter(username=username).exists():
            messages.error("error exists username")
            is_valid = False

        if password != confirm_password:
            messages.error("error password not the same")
            is_valid = False

        if is_valid:

            new_user = User.objects.create(
                user_profile=user_profile,
                username=username,
                email=email,
                password=password,
            )
            new_user.save()

            login_user = authenticate(username=email, password=password)

            login(request, login_user)
            return redirect("core:index")

        else:
            context["username"] = username
            context["email"] = email
            context["userprofile"] = user_profile

    return render(request, "userauths/sign-up.html", context)


def login_view(request):
    # TODO: implement me
    pass
