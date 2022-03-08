from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from instagram .models import Post
from accounts .models import Userprofile
@login_required(login_url= 'login')
def home(request):
    userprofile = Userprofile.objects.get(user_id=request.user.id)
    post = Post.objects.all()
   
    context = {
        'posts' :  post,
        'userprofile' : userprofile,
    }
    return render(request, 'home.html',context)




