from django.shortcuts import get_object_or_404, render, redirect
from .models import Recipe
from .forms import FeedbackForm, RecipeForm

def index(request):
    recipes = Recipe.objects.filter(is_published=True)
    
    context = {
        'title': 'Главная страница',
        'welcome_text': 'Добро пожаловать на наш лучший кулинарный блог!',
        'hero_img': 'images/main.png',
        'hero_title': 'ACooking',
        'hero_accent': 'здоровая еда',
        'hero_description': 'Откройте для себя мир органических рецептов от поваров со всего мира',
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

def recipe_create(request):
    if request.method == 'POST':
        form = RecipeForm(request.POST)
        if form.is_valid():
            recipe = form.save()
            return redirect('recipe_detail', pk=recipe.pk)
    else:
        form = RecipeForm()
    
    context = {
        'form': form,
        'title': 'Создание нового рецепта',
        'button_text': 'Создать рецепт',
    }
    return render(request, 'cooking_blog/recipe_form.html', context)

def recipe_edit(request, pk):
    recipe = get_object_or_404(Recipe, pk=pk)
    
    if request.method == 'POST':
        form = RecipeForm(request.POST, instance=recipe)
        if form.is_valid():
            recipe = form.save()
            return redirect('recipe_detail', pk=recipe.pk)
    else:
        form = RecipeForm(instance=recipe)
    
    context = {
        'form': form,
        'title': 'Редактирование рецепта',
        'button_text': 'Сохранить изменения',
        'recipe': recipe,
    }
    return render(request, 'cooking_blog/recipe_form.html', context)