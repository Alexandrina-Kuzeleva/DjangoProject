from django.contrib import admin
from .models import Recipe, Tag, Comment

@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'difficulty', 'cooking_time', 'is_published', 'created_at', 'author')
    list_filter = ('category', 'difficulty', 'is_published', 'created_at')
    search_fields = ('title', 'description', 'ingredients')
    readonly_fields = ('created_at',)

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('author', 'recipe', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('author__username', 'recipe__title', 'text')
    readonly_fields = ('created_at',)