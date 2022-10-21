from django.shortcuts import render,redirect
from .forms import ReviewForm
from .models import Review
# Create your views here.

def index(request):
    reviews = Review.objects.all()
    context = {
        'reviews': reviews
    }

    return render(request, 'reviews/index.html', context)

def create(request):
    if request.method =='POST':
        review_form = ReviewForm(request.POST)
        if review_form.is_valid():
            form = review_form.save(commit=False)
            form.user = request.user
            form.save()
            return redirect('reviews:index')

    else:   
        review_form = ReviewForm()

    context = {
        'review_form' : review_form
    }
    
    return render(request,'reviews/create.html',context)