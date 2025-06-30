from django.shortcuts import render, redirect
from .models import Post
from .forms import PostForm
from django.contrib import messages

FAKE_NEWS_KEYWORDS = [
    'macron a été vu tout nu',
    'illuminati',
    'reptilien',
    'complot',
    'puce 5G',
    'vaccin tue',
    'plan mondial',
    'gouvernement secret',
    'big pharma',
    'soros',
    'fake',
    'invention',
    'mensonge',
    'la vérité sur',
    'a été vu avec hitler',
    'la fin du monde',
    'eau empoisonnée',
    'nu dans la rue',
    'clone',
    'extraterrestre',
    'censure',
    'ovni',
    'bill gates contrôle le monde'
]


def home(request):
    posts = Post.objects.order_by('-created_at')
    form = PostForm()

    # Marquage des posts suspects
    for post in posts:
        post.is_suspect = any(keyword in post.content.lower() for keyword in FAKE_NEWS_KEYWORDS)

    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('posts:home')

    return render(request, 'posts/home.html', {
        'form': form,
        'posts': posts
    })

