from functools import wraps
from typing import Any
from django.db.models.query import QuerySet
from django.http import Http404, HttpRequest, HttpResponseForbidden, HttpResponseRedirect
from django.http.response import HttpResponse as HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from django.views import View
from .models import BlogPost, User, Comment, UserPicture
from .forms import CreatePostForm, CommentForm, EditPostForm, RegisterForm, UserProfileForm, UserUpdateForm
from django.views.generic import ListView, DetailView, DeleteView, CreateView
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.decorators import method_decorator
from django.core.exceptions import PermissionDenied
from django.views.generic.edit import UpdateView
from django.utils.text import slugify
from django.templatetags.static import static


############# Author only Decorator #############
def author_only(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        post = get_object_or_404(BlogPost, pk=kwargs['pk'])
        if post.author != request.user:
            return render(request, 'blog/not_allowed.html', {"message": "You're not allowed to alter this post"})
        return view_func(request, *args, **kwargs)
    return _wrapped_view


# Create your views here.

# def index(request):
#     posts = BlogPost.objects.all().order_by("-date")[:7]
#     return render(request, "blog/index.html", {
#         "all_posts": posts
#     })

    ################## OR #####################

class IndexView(ListView):
    template_name = "blog/index.html"
    model = BlogPost
    ordering = ["-date"]
    context_object_name = "all_posts"

    def get_queryset(self):
        queryset = super().get_queryset()
        data = queryset[:7]
        return data

def add_new_post(request):
    if request.method == "POST":
        form = CreatePostForm(request.POST, request.FILES)

        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('index')
    
    else:    
        form = CreatePostForm()

    return render(request, "blog/make-post.html", {
        "form": form
    })


# class AddNewPostView(CreateView):
#     model = BlogPost
#     # fields = ['title', 'subtitle', 'image', 'body']
#     template_name = 'blog/make-post.html'
#     context_object_name = 'post'
#     success_url =  reverse_lazy('index')
#     form_class = CreatePostForm


# def edit_post(request, slug):
#     post = get_object_or_404(BlogPost, slug=slug)
#     if request.method == "POST":
#         edit_form = CreatePostForm(request.POST, request.FILES, instance=post)

#         if edit_form.is_valid():
#             edit_form.save()
#             return redirect('index')
    
#     else:
#         edit_form = CreatePostForm(instance=post)  # Prepopulate fields with post data

#     return render(request, "blog/make-post.html", {
#         "form": edit_form
#     })

 ################## OR #####################
@method_decorator([login_required, author_only], name='dispatch')
class EditPostView(UpdateView):
    model = BlogPost
    template_name = 'blog/edit-post.html'
    context_object_name = 'post'
    form_class = EditPostForm


    def get_object(self):
        pk = self.kwargs.get('pk')
        return get_object_or_404(BlogPost, pk=pk)

    def form_valid(self, form):
        post = form.save(commit=False)
        post.save()
        print("Post updated with title:", post.title)  # Debugging output
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('post', args=[self.object.slug])


# @login_required
# def show_post(request, slug):
#     post = get_object_or_404(BlogPost, slug=slug)
#     current_user = request.user
#     if request.method == "POST":
#         comment_form = CommentForm(request.POST)

#         if comment_form.is_valid():
#             comment = comment_form.save(commit=False)
#             comment.blog_post = post
#             # comment.user = current_user
#             comment.save()
            
#             return HttpResponseRedirect(reverse("post", args=[slug]))
      
#     context = {
#         "post": post,
#         "comment_form" : CommentForm()
#     }
#     return render(request, "blog/post.html", context)



    

################## OR #####################

class ShowPostView(View):
    def get(self, request, slug):
        current_user = request.user
        post = get_object_or_404(BlogPost, slug=slug)
        context = {
        "post": post,
        "comment_form" : CommentForm(),
        "comments": post.comments.all().order_by("-id"),
        "current_user": current_user
        }
        return render(request, "blog/post.html", context)


    def post(self, request, slug):
        post = get_object_or_404(BlogPost, slug=slug)
        current_user = request.user
        comment_form = CommentForm(request.POST)

        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.blog_post = post
            comment.user = current_user
            comment.save()
            
            return HttpResponseRedirect(reverse("post", args=[slug]))
        
        context = {
        "post": post,
        "comment_form" : CommentForm(),
        "comments": post.comments.all().order_by("-id"),
        "current_user": current_user
        }
        return render(request, "blog/post.html", context)


class AboutView(View):
    def get(self, request):
        return render(request, "blog/about.html")

################## OR #####################

# def about(request):
#     return render(request, "blog/about.html")


def contact(request):
    return render(request, "blog/contact.html")

@method_decorator([login_required, author_only], name='dispatch')
class PostDeleteView(DeleteView):
    model = BlogPost  
    template_name = "blog/delete.html"  
    success_url = reverse_lazy('index')  
    context_object_name = 'post'



# class UserPictureView( ListView):
#     template_name = "blog/profile_pics.html"
#     model = UserPicture

#     def  get_context_data(self, **kwargs) -> dict[str, Any]:
#         context = super().get_context_data(**kwargs)
#         context["form"] = UserProfileForm()
#         return context


class UserPictureView(UpdateView):
    model = UserPicture
    template_name = "blog/profile_pics.html"
    success_url = reverse_lazy('index') 
    form_class = UserProfileForm
    default_picture_url = static('assets/img/default-profile.jpg')


    def get_object(self, queryset=None):
        # Fetch or create the UserPicture object for the current user
        obj, created = UserPicture.objects.get_or_create(user=self.request.user)
        return obj


#     def form_valid(self, form):
#         # Check if a UserPicture instance already exists for the user
#         user = self.request.user
#         if UserPicture.objects.filter(user=user).exists():
#             # If a UserPicture instance already exists, update it instead
#             user_picture = UserPicture.objects.get(user=user)
#             form.instance = user_picture
#             form.instance.profile_pic = form.cleaned_data.get('profile_pic')
#             form.instance.save()
#             return super().form_valid(form)

#         # Set the user to the currently logged-in user and create a new instance
#         form.instance.user = user
#         return super().form_valid(form)

# class UserPictureView(View):
#     template_name = 'blog/profile_pics.html'
#     default_picture_url = 'static/blog/assets/img/default-profile.jpg'  # Replace with the path to your default picture

#     def get(self, request, *args, **kwargs):
#         user_picture, created = UserPicture.objects.get_or_create(
#             user=request.user,
#             defaults={'profile_pic': self.default_picture_url}
#         )
#         form = UserProfileForm(instance=user_picture)
#         context = {
#             'form': form,
#             'user_picture': user_picture
#         }
#         return render(request, self.template_name, context)

#     def post(self, request, *args, **kwargs):
#         user_picture, created = UserPicture.objects.get_or_create(
#             user=request.user,
#             defaults={'profile_pic': self.default_picture_url}
#         )

#         form = UserProfileForm(request.POST, request.FILES, instance=user_picture)
#         if form.is_valid():
#             form.save()
#             return redirect('index')  # Replace with your desired success URL

#         context = {
#             'form': form,
#             'user_picture': user_picture
#         }
#         return render(request, self.template_name, context)
    
    
def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            # Check if the user already exists
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')

            if User.objects.filter(username=username).exists():
                form.add_error('username', 'Username already exists.')
            elif User.objects.filter(email=email).exists():
                form.add_error('email', 'Email already exists.')
            else:
                # If the user does not exist, save the new user
                user = form.save()
                login(request, user)
                return redirect('index')  # Redirect to home page after registration
    else:
        form = RegisterForm()
    return render(request, 'blog/register.html', {'form': form})


@login_required
def update_user(request):
    if request.method == 'POST':
        form = UserUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('index')  # Redirect to a profile page or similar
    else:
        form = UserUpdateForm(instance=request.user)
    
    return render(request, 'registration/user_update_form.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('index')  # Redirect to home page after logout