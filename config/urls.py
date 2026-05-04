from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from cooking_blog.views import index, categories, recipe_detail, recipe_create, recipe_edit, contact, register, my_recipes, tag_recipes

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index, name='home'),
    path('categories/', categories, name='categories'),
    path('recipe/<int:pk>/', recipe_detail, name='recipe_detail'),
    path('recipe/create/', recipe_create, name='recipe_create'),
    path('recipe/<int:pk>/edit/', recipe_edit, name='recipe_edit'),
    path('contact/', contact, name='contact'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('register/', register, name='register'),
    path('my-recipes/', my_recipes, name='my_recipes'),
    path('tag/<str:slug>/', tag_recipes, name='tag_recipes'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)