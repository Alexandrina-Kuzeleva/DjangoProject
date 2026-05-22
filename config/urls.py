from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from cooking_blog.views import (
    RecipeListView, categories, RecipeDetailView, RecipeCreateView, 
    RecipeUpdateView, RecipeDeleteView, contact, register, 
    MyRecipesListView, TagRecipesListView, add_comment
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', RecipeListView.as_view(), name='home'),  
    path('categories/', categories, name='categories'),
    path('recipe/<int:pk>/', RecipeDetailView.as_view(), name='recipe_detail'),
    path('recipe/create/', RecipeCreateView.as_view(), name='recipe_create'),
    path('recipe/<int:pk>/edit/', RecipeUpdateView.as_view(), name='recipe_edit'),
    path('recipe/<int:pk>/delete/', RecipeDeleteView.as_view(), name='recipe_delete'),
    path('contact/', contact, name='contact'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('register/', register, name='register'),
    path('my-recipes/', MyRecipesListView.as_view(), name='my_recipes'),
    path('tag/<str:slug>/', TagRecipesListView.as_view(), name='tag_recipes'),
    path('recipe/<int:pk>/comment/', add_comment, name='add_comment'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)