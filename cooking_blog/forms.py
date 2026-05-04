from django import forms
from .models import Recipe, Tag

class RecipeForm(forms.ModelForm):
    tags_input = forms.CharField(
        required=False,
        label='Теги',
        help_text='Введите теги через запятую (например: быстрый, завтрак, полезный)',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'быстрый, завтрак, полезный'})
    )
    
    class Meta:
        model = Recipe
        fields = [
            'title',
            'description',
            'ingredients',
            'instructions',
            'cooking_time',
            'category',
            'difficulty',
            'is_published',
            'image',
        ]
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Название блюда'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Краткое описание'}),
            'ingredients': forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'placeholder': 'Список ингредиентов (каждый с новой строки)'}),
            'instructions': forms.Textarea(attrs={'class': 'form-control', 'rows': 8, 'placeholder': 'Пошаговый рецепт приготовления'}),
            'cooking_time': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Время в минутах'}),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'difficulty': forms.Select(attrs={'class': 'form-select'}),
            'is_published': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'title': 'Название рецепта',
            'description': 'Краткое описание',
            'ingredients': 'Ингредиенты',
            'instructions': 'Приготовление',
            'cooking_time': 'Время приготовления (минуты)',
            'category': 'Категория',
            'difficulty': 'Сложность',
            'is_published': 'Опубликовать',
            'image': 'Изображение',
        }

class FeedbackForm(forms.Form):
    subject = forms.CharField(
        max_length=200,
        label='Тема сообщения',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Например: Вопрос о рецепте'})
    )
    email = forms.EmailField(
        label='Ваш Email',
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'example@mail.ru'})
    )
    text = forms.CharField(
        label='Сообщение',
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'placeholder': 'Напишите ваш вопрос или пожелание...'})
    )