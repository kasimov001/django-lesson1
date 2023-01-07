from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect, reverse
from .models import Recipe, Tag, RecipeIngredient
from .forms import RecipeCreateForm, RecipeUpdateForm, TagForm, RecipeIngredientForm
from django.contrib import messages
from django.http import HttpResponse


# recipes -------------------------------------------------
@login_required
def recipe_list(request):
    recipes = Recipe.objects.filter(is_active=True).order_by('-id')
    # qq - Recipe.objects.filter(Q(is_active=True) | Q(tags_title='Salat')).distinct()
    tags_list = Tag.objects.all()
    q = request.GET.get('q')
    tag = request.GET.get('tag')
    # print(tag.split(','))
    if q:
        recipes = recipes.filter(title__icontains=q)
    if tag:
        recipes = recipes.filter(tags__title__exact=tag).distinct()
    ctx = {
        'object_list': recipes,
        'tags_list': tags_list
    }
    return render(request, 'recipe/list.html', ctx)


def recipe_detail(request, slug):
    recipe = get_object_or_404(Recipe, slug=slug)
    ctx = {
        'object': recipe
    }
    return render(request, 'recipe/detail.html', ctx)


@login_required
def recipe_create(request, *args, **kwargs):
    form = RecipeCreateForm()
    if request.method == "POST":
        form = RecipeCreateForm(request.POST or None)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.author = request.user
            obj.is_active = True
            obj.save()
            form.save_m2m()
            return redirect(reverse('recipes:detail', kwargs={"slug": obj.slug}))
            # return redirect('recipes:list')
    ctx = {
        'form': form,
    }
    return render(request, 'recipe/create.html', ctx)


@login_required
def recipe_update(request, slug):
    obj = get_object_or_404(Recipe, slug=slug)
    if request.user != obj.author:
        if not request.user.is_superuser:
            return HttpResponse('<h>Bu Sizga Tegishli Emas!(451)</h>')
    form = RecipeUpdateForm(instance=obj)
    if request.method == "POST":
        form = RecipeUpdateForm(data=request.POST, instance=obj)
    if form.is_valid():
        instance = form.save()
        return redirect("recipes:detail", kwargs={"slug": obj.slug})
    ctx = {
        "form": form
    }
    return render(request, "recipe/update.html", ctx)


@login_required
def recipe_delete(request, slug, ):
    obj = get_object_or_404(Recipe, slug=slug)
    if request.method == "POST":
        obj.delete()
        messages.error(request, f'<b>{obj.title}</b> ochirildi')
        return redirect("recipes:list")
    ctx = {
        'object': obj
    }
    return render(request, 'recipe/delete.html', ctx)


# my recipes -------------------------------------------------
@login_required
def my_recipes(request):
    user = request.user
    recipes = Recipe.objects.filter(author=user)
    tags_list = Tag.objects.all()
    ctx = {
        'object_list': recipes,
        'tags_list': tags_list,
    }
    return render(request, 'recipe/list.html', ctx)


# Tegs ----------------------------------------------------------------
@login_required
def tag_list(request):
    tags = Tag.objects.order_by('-id')
    ctx = {
        'object_list': tags
    }
    return render(request, 'recipe/tag/list.html')


@login_required
def tag_created(request, *args, **kwargs):
    form = TagForm()
    if request.method == "POST":
        form = TagForm(request.POST)
        if form.is_valid():
            obj = form.save()
            return redirect(reverse('recipes:tag_detail'), kwargs={"pk": obj.id})
    ctx = {
        'form': form,
    }
    return render(request, "recipe/tag/create.html", ctx)


def tag_detail(request, pk):
    tag = get_object_or_404(Tag, id=pk)
    ctx = {
        'object': tag
    }
    return request(request, 'recipe/tag/detail.html', ctx)


@login_required
def tag_update(request, pk):
    obj = get_object_or_404(Tag, id=pk)
    form = TagForm(instance=obj)
    if request.method == "POST":
        form = TagForm(data=request.POST, instance=obj)
    if form.is_valid():
        instance = form.save()
        return redirect(reverse("recipes:tag_detail", kwargs={"pk": obj.id}))
    ctx = {
        "form": form
    }
    return render(request, "recipe/tag/update.html", ctx)


@login_required
def tag_delete(request, pk):
    obj = get_object_or_404(Tag, id=pk)
    if request.method == "POST":
        obj.delete()
        messages.error(request, f'<b>{obj.title}</b> ochirildi')
        return redirect("recipes:tag_list")
    ctx = {
        'object': obj
    }
    return render(request, 'recipe/tag/delete.html', ctx)


# ing------------------------------------------------------------------------------
@login_required
def ing_create(request, recipe_slug, *args, **kwargs):
    form = RecipeIngredientForm()
    recipe = get_object_or_404(Recipe, slug=recipe_slug)
    if request.user != recipe.author and not not request.user.is_superuser:
        return HttpResponse('<h>Bu Sizga Tegishli Emas!(451)</h>')
    if request.method == "POST":
        form = RecipeIngredientForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.recipe = recipe
            obj.save()
            return redirect(reverse('recipes:detail'), kwargs={"slug": recipe.slug})
    ctx = {
        'form': form,
    }
    return render(request, "recipe/ing/create.html", ctx)


@login_required
def ing_update(request, recipe_slug, pk):
    obj = get_object_or_404(RecipeIngredient, id=pk)
    recipe = get_object_or_404(Recipe, slug=recipe_slug)
    form = RecipeIngredientForm(instance=obj)
    if request.method == "POST":
        form = RecipeIngredientForm(data=request.POST, instance=obj)
    if form.is_valid():
        instance = form.save()
        return redirect(reverse('recipes:detail'), kwargs={"slug": recipe.slug})
    ctx = {
        "form": form
    }
    return render(request, "recipe/ing/update.html", ctx)


@login_required
def ing_delete(request, recipe_slug, pk):
    obj = get_object_or_404(RecipeIngredient, id=pk)
    recipe = get_object_or_404(Recipe, slug=recipe_slug)
    if request.method == "POST":
        obj.delete()
        messages.error(request, f'<b>{obj.title}</b> ochirildi')
        return redirect(reverse('recipes:detail'), kwargs={"slug": recipe.slug})
    ctx = {
        'object': obj
    }
    return render(request, 'recipe/ing/delete.html', ctx)
