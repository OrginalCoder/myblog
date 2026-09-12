from django.contrib import admin
from .models import Author, Post, Comment

@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ['name', 'user', 'bio']
    search_fields = ['name']

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'created_at', 'updated_at']
    list_filter = ['author', 'created_at']
    search_fields = ['title', 'content']

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['post', 'author', 'content', 'created_at']
    list_filter = ['post', 'author', 'created_at']
    search_fields = ['content']