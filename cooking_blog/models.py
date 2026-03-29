from django.db import models

class Recipe(models.Model): 
    class Category(models.TextChoices):
        BREAKFAST = 'breakfast', 'Завтрак'
        LUNCH = 'lunch', 'Обед'
        DINNER = 'dinner', 'Ужин'
        DESSERT = 'dessert', 'Десерт'
    
    class Difficulty(models.TextChoices):
        EASY = 'easy', 'Простой'
        MEDIUM = 'medium', 'Средний'
        HARD = 'hard', 'Сложный'
    
    title = models.CharField(max_length=200, verbose_name='Название')
    description = models.TextField(verbose_name='Описание')
    ingredients = models.TextField(verbose_name='Ингредиенты')
    instructions = models.TextField(verbose_name='Приготовление')
    cooking_time = models.PositiveIntegerField(verbose_name='Время (мин)')
    category = models.CharField(
        max_length=20,
        choices=Category.choices,
        default=Category.LUNCH,
        verbose_name='Категория'
    )
    difficulty = models.CharField(
        max_length=10,
        choices=Difficulty.choices,
        default=Difficulty.MEDIUM,
        verbose_name='Сложность'
    )
    is_published = models.BooleanField(default=True, verbose_name='Опубликовано')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    
    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'
    
    def __str__(self):
        return self.title