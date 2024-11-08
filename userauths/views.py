from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib import messages
from userauths.models import User


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
            print("new_user")
            print(new_user)
            login(request, new_user)
            return redirect("core:index")

        else:
            context["username"] = username
            context["email"] = email
            context["userprofile"] = user_profile
    print("not ok")
    return render(request, "userauths/sign-up.html", context)


def login_view(request):
    # TODO: implement me
    pass
