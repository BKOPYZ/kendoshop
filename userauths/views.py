from django.shortcuts import render, redirect
from userauths.forms import UserRegisterForm
from django.contrib.auth import login, authenticate


def register_view(request):
    if request.method == "POST":
        # TODO: imeplement in a way that take the input from post
        form = UserRegisterForm(request.POST or None)
        if form.is_valid():
            form.save()
            new_user = authenticate(
                username=form.cleaned_data["email"],
                password=form.cleaned_data["password1"],
            )
            login(request, new_user)
            return redirect("core:index")
    form = UserRegisterForm

    context = {
        "form": form,
    }
    return render(request, "userauths/sign-up.html", context)


def login_view(request):
    # TODO: implement me
    pass
