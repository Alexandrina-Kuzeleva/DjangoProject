from django.shortcuts import render

# Create your views here.

def index(request):
    context = {
        'title': 'Главная страница',
        'welcome_text': 'Добро пожаловать на наш лучший кулинарный блог!',
        'hero_img': 'images/main.png',
        'hero_title': 'ACooking',
        'hero_accent': 'здоровая еда',
        'hero_description': 'Откройте для себя мир органических рецептов от поваров со всего мира',
        'recipes_title': 'Популярные рецепты',
        'recipes_subtitle': 'Лучшие рецепты месяца',
        'recipes': [
            {
                'name': 'Зеленый салат',
                'description': 'Микс из листовых салатов с лимонной заправкой',
                'image': 'images/greensalad.png',
                'button_text': 'Рецепт'
            },
            {
                'name': 'Киноа боул с овощами',
                'description': 'Сытный завтрак из киноа, овощей и тофу, богатый белком и клетчаткой',
                'image': 'images/bowl.png',
                'button_text': 'Рецепт'
            },
            {
                'name': 'Ягодный смузи',
                'description': 'Освежающий смузи из лесных ягод',
                'image': 'images/smoothie.png',
                'button_text': 'Рецепт'
            },
        ]
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
