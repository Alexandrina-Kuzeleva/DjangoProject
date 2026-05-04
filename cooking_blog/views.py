from django.shortcuts import get_object_or_404, render, redirect
from .models import Recipe, Tag
from .forms import FeedbackForm, RecipeForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login as auth_login
from django.contrib.auth.decorators import login_required

def index(request):
    recipes = Recipe.objects.filter(is_published=True)
    
    context = {
        'title': 'Главная страница',
        'welcome_text': 'Добро пожаловать на наш лучший кулинарный блог!',
        'hero_img': 'images/main.png',
        'hero_title': 'ACooking',
        'hero_accent': 'здоровая еда',
        'hero_description': 'Зарегистрируйтесь, чтобы поделиться своим рецептом!',
        'recipes_title': 'Популярные рецепты',
        'recipes_subtitle': f'Всего рецептов: {recipes.count()}',
        'recipes': recipes,
    }
    return render(request, 'cooking_blog/index.html', context)

def categories(request):
    context = {
        'categories': [
            {
                'name': 'Завтраки',
                'description': 'Каши, смузи и полезные сэндвичи',
                'count': 12,
            },
            {
                'name': 'Салаты',
                'description': 'Салаты из свежих овощей, зелени и полезных заправок',
                'count': 8,
            },
            {
                'name': 'Супы',
                'description': 'Лёгкие овощные супы и сытные мясные',
                'count': 6,
            },
        ]
    }
    return render(request, 'cooking_blog/categories.html', context)

def recipe_detail(request, pk):
    recipe = get_object_or_404(Recipe, pk=pk, is_published=True)
    context = {
        'recipe': recipe,
    }
    return render(request, 'cooking_blog/detail.html', context)

def contact(request):
    success = False
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            subject = form.cleaned_data['subject']
            email = form.cleaned_data['email']
            text = form.cleaned_data['text']
            
            print(f'Данные')
            print(f'От: {email}')
            print(f'Тема: {subject}')
            print(f'Сообщение:')
            print(text)
            
            success = True
            form = FeedbackForm()
    else:
        form = FeedbackForm()
    
    context = {
        'form': form,
        'title': 'Свяжитесь с нами',
        'subtitle': 'Задайте вопрос, оставьте отзыв или поделитесь идеей рецепта',
        'success': success,
    }
    return render(request, 'cooking_blog/contact.html', context)

@login_required
def recipe_create(request):
    if request.method == 'POST':
        form = RecipeForm(request.POST, request.FILES)
        if form.is_valid():
            recipe = form.save(commit=False)
            recipe.author = request.user
            recipe.save()
            
            tags_input = form.cleaned_data.get('tags_input')
            if tags_input:
                tag_names = [t.strip().lower() for t in tags_input.split(',')]
                for tag_name in tag_names:
                    tag, created = Tag.objects.get_or_create(name=tag_name)
                    recipe.tags.add(tag)
            
            return redirect('recipe_detail', pk=recipe.pk)
    else:
        form = RecipeForm()
    
    context = {
        'form': form,
        'title': 'Создание нового рецепта',
        'button_text': 'Создать рецепт',
    }
    return render(request, 'cooking_blog/recipe_form.html', context)

@login_required
def recipe_edit(request, pk):
    recipe = get_object_or_404(Recipe, pk=pk)
    
    if recipe.author != request.user:
        return redirect('recipe_detail', pk=pk)
    
    if request.method == 'POST':
        form = RecipeForm(request.POST, request.FILES, instance=recipe)
        if form.is_valid():
            recipe = form.save()
            
            recipe.tags.clear()
            tags_input = form.cleaned_data.get('tags_input')
            if tags_input:
                tag_names = [t.strip().lower() for t in tags_input.split(',')]
                for tag_name in tag_names:
                    tag, created = Tag.objects.get_or_create(name=tag_name)
                    recipe.tags.add(tag)
            
            return redirect('recipe_detail', pk=recipe.pk)
    else:
        initial_tags = ', '.join([tag.name for tag in recipe.tags.all()])
        form = RecipeForm(instance=recipe, initial={'tags_input': initial_tags})
    
    context = {
        'form': form,
        'title': 'Редактирование рецепта',
        'button_text': 'Сохранить изменения',
        'recipe': recipe,
    }
    return render(request, 'cooking_blog/recipe_form.html', context)

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    
    context = {
        'form': form,
        'title': 'Регистрация',
    }
    return render(request, 'registration/register.html', context)

@login_required
def my_recipes(request):
    recipes = Recipe.objects.filter(author=request.user, is_published=True)
    
    context = {
        'title': 'Мои рецепты',
        'recipes': recipes,
        'recipes_title': 'Мои рецепты',
        'recipes_subtitle': f'Всего рецептов: {recipes.count()}',
    }
    return render(request, 'cooking_blog/my_recipes.html', context)

def tag_recipes(request, slug):
    tag = get_object_or_404(Tag, slug=slug)
    recipes = tag.recipes.filter(is_published=True)
    
    context = {
        'tag': tag,
        'recipes': recipes,
        'title': f'Рецепты с тегом: {tag.name}',
        'recipes_title': f'#{tag.name}',
        'recipes_subtitle': f'Найдено рецептов: {recipes.count()}',
    }
    return render(request, 'cooking_blog/tag_recipes.html', context)