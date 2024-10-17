from django.http import Http404
from django.shortcuts import get_object_or_404
from django.http import HttpResponse

from django.shortcuts import render, redirect
from django.core.exceptions import ObjectDoesNotExist

from django.contrib import auth

from django.contrib.auth.decorators import login_required

from MainApp.models import Snippet
from MainApp.forms import SnippetForm, UserRegistrationForm

def index_page(request):
    context = {'pagename': 'PythonBin'}
    return render(request, 'pages/index.html', context)


@login_required
def my_snippets(request):
    context = {
        'pagename': 'Мои сниппеты',
        'snippets': Snippet.objects.filter(user=request.user)
        }
    return render(request, 'pages/view_snippets.html', context)



def snippets_page(request):
    context = {
        'pagename': 'Просмотр сниппетов',
        'snippets': Snippet.objects.filter(public=True)
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
        context["type"] = "view"
        return render(request, 'pages/snippet_detail.html', context)


@login_required(login_url='home')
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
           snippet = form.save(commit=False)
           if request.user.is_authenticated:
               snippet.user = request.user
               snippet.save()
           return redirect("snippets-list")
       return render(request,'pages/add_snippet.html', {'form': form})


@login_required
def snippet_edit(request, snippet_id):
    context = {'pagename': 'Редактирование сниппета'}
    snippet = get_object_or_404(Snippet.objects.filter(user=request.user), id=snippet_id)
    # 1 вариант - использование SnippetForm
    if request.method == "GET":
        form = SnippetForm(instance=snippet)
        return render(request, "pages/add_snippet.html", context | {"form": form})
    
    # 2 вариант
    # Получаем страница с данными сниппета
    # if request.method == "GET":
    #     context.update({
    #         "snippet": snippet,
    #         "type": "edit",
    #         })
    #     return render(request, 'pages/snippet_detail.html', context)
    
    # Получаем данные из формы и на их основе обновляем данный сниппет в БД
    if request.method == "POST":
        data_form = request.POST
        snippet.name = data_form["name"]
        snippet.code = data_form["code"]
        snippet.public = data_form.get('public', False)  # Checkbox ничего не передает, если не отмечен!!! 
        snippet.save()
        return redirect("snippets-list") # GET /snippets/list


@login_required
def snippet_delete(request, snippet_id):
    if request.method == "GET" or request.method == "POST":
        snippet = get_object_or_404(Snippet.objects.filter(user=request.user), id=snippet_id)
        snippet.delete()
    return redirect("snippets-list")


def login(request):
    if request.method == 'POST':
        username = request.POST.get("username")
        password = request.POST.get("password")
        # print("username =", username)
        # print("password =", password)
        # return HttpResponse(f"username = {username}; password = {password}")
        user = auth.authenticate(request, username=username, password=password)
        if user is not None:
            auth.login(request, user)
        else:
            # Return error message
            context = {
               'pagename': 'Редактирование сниппета',
               'errors': ['wrond name or password']
            }
            return render(request, 'pages/index.html', context)
    # return redirect('home')
    return redirect(request.META.get('HTTP_REFERER', '/'))  # на ту страницу, на которой вы логинились


def logout(request):
    auth.logout(request)
    return redirect('home')


def create_user(request):
    context = {"pagename": "Регистрация нового пользователя"}
    # Создаем новую форму при запросе GET
    if request.method == "GET":
        form = UserRegistrationForm()
    
    # Получаем данные из формы и на их основе создаем нового пользователя и сохраняем его в БД
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("home")
        
    context['form'] = form
    return render(request, "pages/registration.html", context)
