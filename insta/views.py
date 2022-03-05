from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from instagram .models import Post

@login_required(login_url= 'login')
def home(request):
    post = Post.objects.all()
    context = {
        'posts' :  post,
    }
    return render(request, 'home.html',context)

