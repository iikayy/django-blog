from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from django.contrib.auth import get_user_model
from django.templatetags.static import static

# Create your models here.


#################### CUSTOM USER MODEL#######################
# class User(models.Model):
#     email = models.EmailField()
#     password = models.CharField(max_length=200)
#     username = models.CharField(max_length=200)
#     profile_pic = models.ImageField(upload_to="profile_pics", null=True)

    
    # def __str__(self):
    #     return f"{self.username}"



############################ DJANGO DEFAULT MODEL   ##################################
User = get_user_model()


class BlogPost(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_posts')
    title = models.CharField(max_length=200)
    subtitle = models.CharField(max_length=200)
    date = models.DateField(auto_now=True)
    body = models.TextField()
    image= models.ImageField(upload_to="posts_pics", null=True)
    slug = models.SlugField(unique=True, db_index=True)
    

    # def __str__(self):
    #     return f"{self.author} {self.title}"

    def get_absolute_url(self):
        return reverse("post", args=[self.slug])


    def save(self, *args, **kwargs):
        if not self.slug or self.pk is None:
            # Only generate a new slug if it's a new instance or slug is missing
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments', null=True)
    blog_post = models.ForeignKey(BlogPost, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField()


class UserPicture(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='user_pics')
    profile_pic = models.ImageField(upload_to='profile_pics', null=True, blank=True)

    def __str__(self):
        return self.user.username
    
    def save(self, *args, **kwargs):
        if not self.profile_pic:
            self.profile_pic = None  # Clear any wrongly set media paths
        super().save(*args, **kwargs)

    @property
    def picture_url(self):
        # Return the uploaded picture if it exists, otherwise return the static default image
        if self.profile_pic:
            return self.profile_pic.url
        return static('assets/img/default-profile.jpg')