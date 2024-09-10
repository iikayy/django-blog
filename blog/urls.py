from django.urls import path
from .views import *
from django.contrib.auth.views import LoginView, PasswordChangeView, PasswordChangeDoneView

urlpatterns = [

    path("", IndexView.as_view(), name="index"),
    # path("", views.index, name="index"),
    path("about", AboutView.as_view(), name="about"),
    # path("about", views.about, name="about"),
    path("post/<slug:slug>", ShowPostView.as_view(), name="post"),
    # path("post/<slug:slug>",views.show_post, name="post"),
    path("edit-post/<int:pk>",EditPostView.as_view(), name="edit-post"),
    # path("edit-post/<slug:slug>", edit_post, name="edit-post"),
    # path("new-post/", AddNewPostView.as_view(), name="new-post"),
    path("new-post/",  add_new_post, name="new-post"),
    path('register/', register, name='register'),
    path('login/', LoginView.as_view(template_name='blog/login.html'), name='login'),
    path('logout/', logout_view, name='logout'),
    path("delete/<int:pk>", PostDeleteView.as_view(), name='delete'),
    path('password_change/',  PasswordChangeView.as_view(template_name='registration/password_change_form.html', success_url=reverse_lazy('password_change_done')), name='password_change'),
    path('password_change/done/', PasswordChangeDoneView.as_view(template_name='registration/password_change_done.html'),  name='password_change_done'),
    path('profile_pics/<int:pk>', UserPictureView.as_view(), name='profile_pics_with_pk'),
    path('profile_pics/', UserPictureView.as_view(), name='profile_pics'),
    path('update_user/', update_user, name='update_profile'),
    path("contact", contact, name="contact")

]
