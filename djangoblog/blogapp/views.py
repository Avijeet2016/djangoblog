from django.shortcuts import render, HttpResponse, get_object_or_404, redirect
from .models import Author, Category, Article, Comment
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db.models import Q
from .forms import createForm, registerUser, createAuthor, commentForm
from django.contrib import messages

# Create your views here.
def index(request):
    post = Article.objects.all().order_by('-id')
    search = request.GET.get('q')
    if search:
        post = post.filter(
            Q(title__icontains=search)|     # __ double underscore দিতে হবে কিন্তু
            Q(body__icontains=search)     # এবং | দিতে হবে seperation এর জন্য
        )
    paginator = Paginator(post, 25) # Show 25 contacts per page

    page = request.GET.get('page')
    total_article = paginator.get_page(page)
    context = {
        'post': total_article
    }
    return render(request, "index.html", context)

def getauthor(request, name):
    post_author = get_object_or_404(User, username=name)
    auth = get_object_or_404(Author, name=post_author.id)
    post = Article.objects.filter(article_author=auth.id)
    paginator = Paginator(post, 3) # Show 25 contacts per page

    page = request.GET.get('page')
    total_article = paginator.get_page(page)
    context = {
        'auth': auth,
        'post': total_article
    }
    return render(request, "profile.html", context)

def getsingle(request, id):
    post = get_object_or_404(Article, pk=id)
    first = Article.objects.first()
    last = Article.objects.last()
    getComment = Comment.objects.filter(post=id)
    related = Article.objects.filter(category=post.category).exclude(id=id)[:4]
    form = commentForm(request.POST or None)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.post = post
        instance.save()
    context = {
        'post': post,
        'first': first,
        'last': last,
        'related': related,
        'form': form,
        'comment': getComment
    }
    return render(request, "single.html", context)

def getTopic(request, name):
    cat = get_object_or_404(Category, name=name)
    post = Article.objects.filter(category=cat.id)
    paginator = Paginator(post, 3) # Show 25 contacts per page

    page = request.GET.get('page')
    total_article = paginator.get_page(page)
    context = {
        'post': total_article,
        'cat': cat
    }
    return render(request, 'category.html', context)

def getLogin(request):
    if request.user.is_authenticated:  # যদি লগিন করা থাকে
        return redirect('index')
    else:                              # যদি লগিন করা না থাকে তাহলে লগিন করবে
        if request.method == "POST":
            user = request.POST.get('user')
            password = request.POST.get('pass')
            auth = authenticate(request, username=user, password=password)
            if auth is not None:
                login(request, auth)
                return redirect('index')
            else:
                messages.add_message(request, messages.ERROR, 'Username or Password mismatch')
                return render(request, 'login.html')

    return render(request, 'login.html')

def getLogout(request):
    logout(request)
    return redirect("index")

def getCreate(request):
    if request.user.is_authenticated:
        u = get_object_or_404(Author, name=request.user.id)
        form = createForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.article_author = u
            instance.save()
            messages.success(request, 'Post is published successfully')
            return redirect('profile')
        context = {
            'form': form
        }
        return render(request, "create.html", context)
    else:
        return redirect('index')

def getProfile(request):
    if request.user.is_authenticated:
        user = get_object_or_404(User, id=request.user.id)
        author_profile = Author.objects.filter(name=user.id)
        if author_profile:
            authorUser = get_object_or_404(Author, name=request.user.id)
            post = Article.objects.filter(article_author=authorUser.id)
            context = {
                'post': post,
                'user': authorUser
            }
            return render(request, 'logged_in_profile.html', context)
        else:
            form = createAuthor(request.POST or None,request.FILES or None)
            if form.is_valid():
                instance = form.save(commit=False)
                instance.name = user
                instance.save()
                messages.success(request, 'Author profile is created successfully')
                return redirect('profile')
            return render(request, 'createauthor.html', {'form': form})
    else:
        return render('login')

def getUpdate(request, id):
    if request.user.is_authenticated:
        u = get_object_or_404(Author, name=request.user.id)
        post = get_object_or_404(Article, id=id)
        form = createForm(request.POST or None, request.FILES or None, instance=post)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.article_author = u
            instance.save()
            messages.success(request, 'Post is successfully updated')
            return redirect('profile')
        context = {
            'form': form
        }
        return render(request, "create.html", context)
    else:
        return redirect('index')

def getDelete(request, id):
    if request.user.is_authenticated:
        post = get_object_or_404(Article, id=id)
        post.delete()
        messages.warning(request, 'Post is deleted')
        return redirect('profile')
    else:
        return redirect('index')

def getRegister(request):
    form = registerUser(request.POST or None)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        messages.success(request, 'Registration successfully completed')
        return redirect('login')
    context = {
        'form': form
    }
    return render(request, 'register.html', context)

