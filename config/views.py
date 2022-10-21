from django.shortcuts import render, redirect


def main(request):
    if request.user.is_authenticated:
        return redirect("reviews:index")
    else:
        return redirect("accounts:login")
