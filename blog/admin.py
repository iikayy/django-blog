from django.contrib import admin

from .models import BlogPost, Comment, UserPicture

# Register your models here.

class BlogPostAdmin(admin.ModelAdmin):
    prepopulated_fields={"slug":("title",)}
    list_filter = ("author", "title", "date",)
    list_display = ("title", "author", "date")

admin.site.register(BlogPost, BlogPostAdmin)
# admin.site.register(User)
admin.site.register(Comment)
admin.site.register(UserPicture)