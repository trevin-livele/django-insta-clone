from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from .models import Post


def createpost(request):
    if request.method == 'POST':
        image = request.FILES.get('image')
        description = request.POST.get('description')
        post = Post.objects.create(user=request.user,image=image,description=description)
        post.save()
        return redirect('dash')
    return render(request, 'create_post.html')
