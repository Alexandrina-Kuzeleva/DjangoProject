from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login as auth_login
from django.contrib import messages
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Recipe, Tag, Comment
from .forms import RecipeForm, FeedbackForm, CommentForm

class RecipeListView(ListView):
    model = Recipe
    template_name = 'cooking_blog/index.html'
    context_object_name = 'recipes'
    ordering = ['-created_at']
    
    def get_queryset(self):
        return Recipe.objects.filter(is_published=True)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Главная страница'
        context['welcome_text'] = 'Добро пожаловать на наш лучший кулинарный блог!'
        context['hero_img'] = 'images/main.png'
        context['hero_title'] = 'ACooking'
        context['hero_accent'] = 'здоровая еда'
        context['hero_description'] = 'Откройте для себя мир органических рецептов от поваров со всего мира'
        context['recipes_title'] = 'Популярные рецепты'
        context['recipes_subtitle'] = f'Всего рецептов: {self.get_queryset().count()}'
        return context
    
class RecipeDetailView(DetailView):
    model = Recipe
    template_name = 'cooking_blog/detail.html'
    context_object_name = 'recipe'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comment_form'] = CommentForm()
        return context

class RecipeCreateView(LoginRequiredMixin, CreateView):
    model = Recipe
    form_class = RecipeForm
    template_name = 'cooking_blog/recipe_form.html'
    success_url = reverse_lazy('home')
    
    def form_valid(self, form):
        recipe = form.save(commit=False)
        recipe.author = self.request.user
        recipe.save()
        
        tags_input = form.cleaned_data.get('tags_input')
        if tags_input:
            tag_names = [t.strip().lower() for t in tags_input.split(',')]
            for tag_name in tag_names:
                tag, created = Tag.objects.get_or_create(name=tag_name)
                recipe.tags.add(tag)
        
        messages.success(self.request, f'Рецепт "{recipe.title}" успешно создан!')
        return redirect('recipe_detail', pk=recipe.pk)
    
    def form_invalid(self, form):
        messages.error(self.request, 'Ошибка при создании рецепта. Проверьте заполнение полей.')
        return super().form_invalid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Создание нового рецепта'
        context['button_text'] = 'Создать рецепт'
        return context

class RecipeUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Recipe
    form_class = RecipeForm
    template_name = 'cooking_blog/recipe_form.html'
    
    def test_func(self):
        recipe = self.get_object()
        return self.request.user == recipe.author
    
    def form_valid(self, form):
        recipe = form.save()
        
        recipe.tags.clear()
        tags_input = form.cleaned_data.get('tags_input')
        if tags_input:
            tag_names = [t.strip().lower() for t in tags_input.split(',')]
            for tag_name in tag_names:
                tag, created = Tag.objects.get_or_create(name=tag_name)
                recipe.tags.add(tag)
        
        messages.success(self.request, f'Рецепт "{recipe.title}" успешно обновлён!')
        return redirect('recipe_detail', pk=recipe.pk)
    
    def form_invalid(self, form):
        messages.error(self.request, 'Ошибка при обновлении рецепта.')
        return super().form_invalid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Редактирование рецепта'
        context['button_text'] = 'Сохранить изменения'
        
        if self.object:
            initial_tags = ', '.join([tag.name for tag in self.object.tags.all()])
            context['form'].fields['tags_input'].initial = initial_tags
        
        return context

class RecipeDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Recipe
    template_name = 'cooking_blog/recipe_confirm_delete.html'
    success_url = reverse_lazy('home')
    
    def test_func(self):
        recipe = self.get_object()
        return self.request.user == recipe.author
    
    def delete(self, request, *args, **kwargs):
        recipe = self.get_object()
        messages.success(request, f'Рецепт "{recipe.title}" успешно удалён!')
        return super().delete(request, *args, **kwargs)

class MyRecipesListView(LoginRequiredMixin, ListView):
    model = Recipe
    template_name = 'cooking_blog/my_recipes.html'
    context_object_name = 'recipes'
    
    def get_queryset(self):
        return Recipe.objects.filter(author=self.request.user, is_published=True)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Мои рецепты'
        context['recipes_title'] = 'Мои рецепты'
        context['recipes_subtitle'] = f'Всего рецептов: {self.get_queryset().count()}'
        return context

class TagRecipesListView(ListView):
    model = Recipe
    template_name = 'cooking_blog/tag_recipes.html'
    context_object_name = 'recipes'
    
    def get_queryset(self):
        self.tag = get_object_or_404(Tag, slug=self.kwargs.get('slug'))
        return self.tag.recipes.filter(is_published=True)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tag'] = self.tag
        context['title'] = f'Рецепты с тегом: {self.tag.name}'
        context['recipes_title'] = f'#{self.tag.name}'
        context['recipes_subtitle'] = f'Найдено рецептов: {self.get_queryset().count()}'
        return context

def add_comment(request, pk):
    recipe = get_object_or_404(Recipe, pk=pk)
    
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.recipe = recipe
            comment.save()
            messages.success(request, 'Ваш комментарий успешно добавлен!')
        else:
            messages.error(request, 'Ошибка при добавлении комментария. Попробуйте снова.')
        
        return redirect('recipe_detail', pk=pk)

def contact(request):
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            subject = form.cleaned_data['subject']
            email = form.cleaned_data['email']
            text = form.cleaned_data['text']
            
            print('=' * 50)
            print(f'НОВОЕ СООБЩЕНИЕ С САЙТА ACooking')
            print(f'От: {email}')
            print(f'Тема: {subject}')
            print(f'Сообщение:')
            print(text)
            print('=' * 50)
            
            messages.success(request, 'Ваше сообщение успешно отправлено! Мы ответим вам в ближайшее время.')
            return redirect('contact')
        else:
            messages.error(request, 'Ошибка при отправке сообщения. Проверьте правильность заполнения полей.')
    else:
        form = FeedbackForm()
    
    context = {
        'form': form,
        'title': 'Свяжитесь с нами',
        'subtitle': 'Задайте вопрос, оставьте отзыв или поделитесь идеей рецепта',
    }
    return render(request, 'cooking_blog/contact.html', context)

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            messages.success(request, f'Добро пожаловать, {user.username}! Регистрация прошла успешно.')
            return redirect('home')
        else:
            messages.error(request, 'Ошибка регистрации. Проверьте правильность заполнения полей.')
    else:
        form = UserCreationForm()
    
    context = {
        'form': form,
        'title': 'Регистрация',
    }
    return render(request, 'registration/register.html', context)

def categories(request):
    context = {
        'categories': [
            {'name': 'Завтраки', 'description': 'Каши, смузи и полезные сэндвичи', 'count': 12},
            {'name': 'Салаты', 'description': 'Салаты из свежих овощей, зелени и полезных заправок', 'count': 8},
            {'name': 'Супы', 'description': 'Лёгкие овощные супы и сытные мясные', 'count': 6},
        ]
    }
    return render(request, 'cooking_blog/categories.html', context)