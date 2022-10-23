from datetime import datetime
from django.shortcuts import render, redirect
from django.http import HttpResponseForbidden
from .forms import ReviewForm, CommentForm
from .models import Review, Comment
from django.contrib.auth.decorators import login_required

# Create your views here.


@login_required
def index(request):
    reviews = Review.objects.all().order_by("-pk")
    context = {
        "reviews": reviews,
    }

    return render(request, "reviews/index.html", context)


@login_required
def create(request):
    if request.method == "POST":
        review_form = ReviewForm(request.POST)
        if review_form.is_valid():
            form = review_form.save(commit=False)
            form.user = request.user
            form.save()
            return redirect("reviews:index")

    else:
        review_form = ReviewForm()

    context = {
        "review_form": review_form,
    }

    return render(request, "reviews/create.html", context)


def detail(request, review_pk):
    review = Review.objects.get(pk=review_pk)
    comment_form = CommentForm()
    context = {
        "review": review,
        "comment_form": comment_form,
        "comments": review.comment_set.all(),
    }
    return render(request, "reviews/detail.html", context)


@login_required
def update(request, review_pk):
    review = Review.objects.get(pk=review_pk)
    if review.user == request.user:

        if request.method == "POST":
            review_form = ReviewForm(request.POST, instance=review)
            if review_form.is_valid():
                form = review_form.save(commit=False)
                form.user = request.user
                form.save()
                return redirect("reviews:detail", review.pk)

        else:
            review_form = ReviewForm(instance=review)

        context = {
            "review_form": review_form,
        }

        return render(request, "reviews/update.html", context)

    else:
        return HttpResponseForbidden()


@login_required
def delete(request, review_pk):
    review = Review.objects.get(pk=review_pk)
    if review.user == request.user:
        review.delete()
        return redirect("reviews:index")
    else:
        return HttpResponseForbidden()


@login_required
def comments_create(request, review_pk):
    review = Review.objects.get(pk=review_pk)
    if request.user.is_authenticated:
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.review = review
            comment.user = request.user
            comment.save()
        return redirect("reviews:detail", review.pk)


@login_required
def comments_delete(request, review_pk, comment_pk):
    comment = Comment.objects.get(pk=comment_pk)

    if request.user == comment.user:
        comment.delete()
        return redirect("reviews:detail", review_pk)
    else:
        return HttpResponseForbidden()
