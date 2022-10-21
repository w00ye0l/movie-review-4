from xml.etree.ElementTree import Comment
from django.forms import ModelForm
from .models import Review, Comment


class ReviewForm(ModelForm):
    class Meta:
        model = Review
        fields = "__all__"
        exclude = ("user",)
        labels = {
            "title": "리뷰 제목",
            "content": "리뷰 내용",
            "grade": "영화 평점",
            "movie_name": "영화 이름",
        }


class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ("content",)
