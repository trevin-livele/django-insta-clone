from email import message
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from .models import Post,Comment


def createpost(request):
    if request.method == 'POST':
        image = request.FILES.get('image')
        description = request.POST.get('description')
        post = Post.objects.create(user=request.user,image=image,description=description)
        post.save()
        return redirect('home')
    return render(request, 'create_post.html')


def comment(request,pk):
    post = Post.objects.get(pk=pk)
    if request.method == 'POST':
        comment = request.POST.get('comment')
        comments = Comment.objects.create(user=request.user, 
                                          message_body=comment,
                                          post=post)
        return redirect('home')
    return render(request, 'home.html')


def profile(request):
    return render(request, 'profile.html')