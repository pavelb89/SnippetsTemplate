from django.http import Http404
from django.shortcuts import render, redirect
from django.core.exceptions import ObjectDoesNotExist

from MainApp.models import Snippet
from MainApp.forms import SnippetForm

def index_page(request):
    context = {'pagename': 'PythonBin'}
    return render(request, 'pages/index.html', context)


def snippets_page(request):
    context = {
        'pagename': 'Просмотр сниппетов',
        'snippets': Snippet.objects.all()
        }
    return render(request, 'pages/view_snippets.html', context)


def snippet_detail(request, snippet_id: int):
    context = {'pagename': 'Просмотр сниппета'}
    try:
        snippet = Snippet.objects.get(id=snippet_id)
    except ObjectDoesNotExist:
        return render(request, 'pages/errors.html', context | {'error': f'Ошибка! Сниппет с id={snippet_id} не найден!'})
    else:
        context['snippet'] = snippet
        return render(request, 'pages/snippet_detail.html', context)


def add_snippet_page(request):
    if request.method == "GET":
        form = SnippetForm()
        context = {
            'pagename': 'Добавление нового сниппета',
            'form': form
        }
        return render(request, 'pages/add_snippet.html', context)

    if request.method == "POST":
       form = SnippetForm(request.POST)
       if form.is_valid():
           form.save()
           return redirect("snippets-list")
       return render(request,'pages/add_snippet.html',{'form': form})

