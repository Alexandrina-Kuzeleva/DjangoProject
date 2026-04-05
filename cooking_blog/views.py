from django.shortcuts import render
from .models import Recipe

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