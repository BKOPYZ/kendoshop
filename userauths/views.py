from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from userauths.models import User
from django.core.files import File
from django.contrib.auth.decorators import login_required, user_passes_test


def register_view(request):
    if request.user.is_authenticated:
        return redirect("core:home")

    context = dict()
    if request.method == "POST" and request.POST.get("submit", False):
        post = request.POST
        first_name = post.get("firstname", None)
        last_name = post.get("lastname", None)

        username = post.get("username")
        email = post.get("email")
        password = post.get("password")
        confirm_password = post.get("confirm_password")

        context["username"] = username
        context["email"] = email

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
                    username=username,
                    email=email,
                    first_name=first_name,
                    last_name=last_name,
                )
                user_profile = request.FILES.get("user_profile", None)
                context["userprofile"] = user_profile

                is_profile_None = False

                if user_profile is None:
                    with open("../static/assets/imgs/human.png", "rb") as f:
                        user_profile = f.read()
                    is_profile_None = True

                new_user.user_profile = user_profile
                if not is_profile_None:
                    new_user.user_profile.save(
                        "user_profile.png",
                        File(user_profile),
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
                print(e)
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
        except User.DoesNotExist:
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
    messages.success(request, "You have logout")
    return redirect("userauths:login")


@login_required(login_url="userauths:login")
def profile_view(request):
    return render(request, "userauths/profile.html", {})


@login_required(redirect_field_name="userauths:login")
def edit_profile_view(request):

    context = dict()

    if request.method == "POST":
        post = request.POST

        first_name = post.get("firstname")
        last_name = post.get("lastname")
        email = post.get("email")

        context["firstname"] = first_name
        context["lastname"] = last_name
        context["email"] = email

        user = User.objects.filter(email=email)

        if user.exists() and user[0].user_id != request.user.user_id:
            context["email"] = ""
            messages.error("this email has been used")

        else:
            user = User.objects.get(user_id=request.user.user_id)
            user.email = email
            user.first_name = first_name
            user.last_name = last_name
            user_profile = request.FILES.get("user_profile", None)
            context["userprofile"] = user_profile

            is_profile_None = False

            if user_profile is None:
                with open("../static/assets/imgs/human.png", "rb") as f:
                    user_profile = f.read()
                is_profile_None = True

            user.user_profile = user_profile
            if not is_profile_None:
                user.user_profile.save(
                    "user_profile.png",
                    File(user_profile),
                )
            user.save()
            messages.success(request, "success")
            return redirect("userauths:profile")

    return render(request, "userauths/edit_profile.html", {})
