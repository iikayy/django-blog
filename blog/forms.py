from django import forms
from .models import BlogPost, Comment, UserPicture
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm


# class CreatePostForm(forms.Form):
#     title = forms.CharField(label="Title", max_length=200)
#     subtitle = forms.CharField(label="Subtitle", max_length=200)
#     image = forms.ImageField()
#     body = forms.CharField(label="Body", widget=forms.Textarea)

class CreatePostForm(forms.ModelForm):
    class Meta:
        model = BlogPost
        fields = ['title', 'subtitle', 'image', 'body']
        labels = {
            "title": "Title",
            "subtitle" : "Subtitle",
            "image" : "Image",
            "body": "Body",
        }

class EditPostForm(forms.ModelForm):
    class Meta:
        model = BlogPost
        fields = ['title', 'subtitle', 'image', 'body']
        labels = {
            "title": "Title",
            "subtitle" : "Subtitle",
            "image" : "Image",
            "body": "Body",
        }


class RegisterForm(UserCreationForm):
    # email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username',  'email']
    


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
        labels = {
            "text": "Comment"
        }

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserPicture
        fields = ['profile_pic']
        labels = {
            'profile_pic': "Image",
        }