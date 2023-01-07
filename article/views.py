from django.contrib.auth.decorators import login_required
from django.core.checks import messages
from django.shortcuts import render, Http404, redirect, reverse, HttpResponse
from .models import Article
import random
from .forms import Articleform
from django.contrib.auth.models import User
from django.contrib import messages

# Create your views here.
# def index(request):
#     return render(request, "article/index.html")


def index(request):
    articles = Article.objects.filter(is_deleted__exact=False).order_by('-id')
    q = request.GET.get('q')
    if q:
        articles = articles.filter(title__icontains=q)
        # print(articles.query)
    return render(request, "article/index.html", {"object_list": articles})


def detail(request, slug=None):
    context = {}
    if slug:
        article = Article.objects.get(slug=slug)
        context["object"] = article
        return render(request, 'article/detail.html', context)

    return Http404()


def _create(request):
    context = {
'created': False

    }
    if request.method == "POST":
        title = request.POST.get('title')
        content = request.POST.get("content")
        article = Article.objects.create(title=title, content=content)
        context['object'] = article
        context['created'] = True
        # return redirect(reverse("articles:detail", kwargs={"pk": article.id}))
    return render(request, 'article/create.html', context)


@login_required
def create_1(request):
    form=Articleform()
    context = {
        'form': form
    }
    if request.method == 'POST':
        form = Articleform(request.POST, files=request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "article Created")
        context['object'] = form.data
        context['created'] = True

    return render(request, 'article/create.html', context)


def create(request):
    form = Articleform(request.POST or None, files=request.FILES)
    if form.is_valid():
        form.save()
        return redirect('articles:list')
    context = {
        'form': form
    }
    return render(request, 'article/create.html', context)



# def __create(request):
#     form = Articleform(request.POST or None)
#     if form.is_valid():
#         form.save()
#         return redirect('articles:list')
#     context = {
#         'form': form
#     }
#     return render(request, 'article/create.html', context)

@login_required
def edit(request, slug):
    article = Article.objects.get(slug=slug)
    form = Articleform(instance=article)
    if request.method == "POST":
        form = Articleform(data=request.POST, instance=article, files=request.FILES)
        form.save()
        return redirect(reverse('articles:detail', kwargs={"slug": article.slug}))
    ctx = {
        'form': form
    }
    return render(request, 'article/edit.html', ctx)

@login_required
def delete(request, slug):
    article = Article.objects.get(slug=slug)
    if request.method == "POST":
        # article.delete()
        article.is_deleted = True
        article.save()
        messages.success(request, f"article deleted ({article.id})")
        return redirect("articles:list")
    context = {
        "object": article
    }
    return render(request, "article/delete.html", context)
