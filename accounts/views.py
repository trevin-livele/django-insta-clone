from django.shortcuts import redirect, render,get_object_or_404
from accounts.models import Account
from instagram .models import Post
from .forms import RegistrationForm,UserForm,UserprofileForm
from.models import Account, FollowersCount,Userprofile
from django.contrib import messages,auth
from django.contrib.auth.decorators import login_required


#email verification
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage

# Create your views here.

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            phone_number = form.cleaned_data['phone_number']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            username = email.split("@")[0]
            user = Account.objects.create_user(first_name=first_name,last_name=last_name,
                                                email=email,username=username,password=password)
            user.phone_number = phone_number
            user.save()


            # Create a user profile
            profile = Userprofile()
            profile.user_id = user.id
            profile.profile_picture = 'default/default-user.jpg'
            profile.save()


            #USER ACTIVATION
            current_site = get_current_site(request)
            mail_subject = 'please activate your account'
            message = render_to_string('accounts/account_verification_email.html',{
                'user' : user,
                'domain' : current_site,
                'uid' : urlsafe_base64_encode(force_bytes(user.pk)),
                'token' : default_token_generator.make_token(user),
            })
            to_email = email
            send_email = EmailMessage(mail_subject, message, to=[to_email])
            send_email.send()
            return redirect('/accounts/login/?command=verification&email='+email)
    else:
        form = RegistrationForm()
    context = {
        'form' : form,
    }
    return render(request, 'accounts/register.html' ,context)


def login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        user = auth.authenticate(email=email,password=password)

        if user is not None:
            auth.login(request, user)
            messages.success(request, 'You are now logged in.')
            return redirect('home')
        else:
            messages.error(request, 'Invalid login credentials')
            return redirect('login')
    return render(request, 'accounts/login.html')

@login_required(login_url = 'login')
def logout(request):
    auth.logout(request)
    messages.success(request, 'You are logged out.')
    return redirect('login')

def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, Account.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, 'Congratulations! Your account is activated.')
        return redirect('login')
    else:
        messages.error(request, 'Invalid activation link')
        return redirect('register')




@login_required(login_url= 'login')
def dashboard(request):
    return render(request, 'accounts/dashboard.html')
    







def forgotpassword(request):
    if request.method == 'POST':
        email = request.POST['email']
        if Account.objects.filter(email=email).exists():
            user = Account.objects.get(email__exact=email)
            #reset password email
            current_site = get_current_site(request)
            mail_subject = 'Reset your password'
            message = render_to_string('accounts/reset_password_email.html',{
                'user' : user,
                'domain' : current_site,
                'uid' : urlsafe_base64_encode(force_bytes(user.pk)),
                'token' : default_token_generator.make_token(user),
            })
            to_email = email
            send_email = EmailMessage(mail_subject, message, to=[to_email])
            send_email.send()

            messages.success(request, 'password reset email has been sent to your email address')
            return redirect('login')


        else:
            messages.error(request, 'Account does not exist')
            return redirect('forgotpassword')
    return render(request, 'accounts/forgotpassword.html')




def resetpassword_validate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, Account.DoesNotExist):
        user = None
    
    if user is not None and default_token_generator.check_token(user, token):
        request.session['uid'] = uid
        messages.success(request, 'please reset your password')
        return redirect('resetpassword')
    else:
        messages.error(request, 'this link has expired')
    return redirect('login')





def resetpassword(request):
    if request.method == 'POST':
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password == confirm_password:
            uid = request.session.get('uid')
            user = Account.objects.get(pk=uid)
            user.set_password(password)
            user.save()
            messages.success(request, 'Password reset successful')
            return redirect('login')
        else:
            messages.error(request, 'Password do not match!')
            return redirect('resetpassword')
    else:
        return render(request, 'accounts/resetpassword.html')




@login_required(login_url='login')
def edit_profile(request):
    userprofile = get_object_or_404(Userprofile, user=request.user)
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = UserprofileForm(request.POST, request.FILES, instance=userprofile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your profile has been updated.')
            return redirect('edit_profile')
    else:
        user_form = UserForm(instance=request.user)
        profile_form = UserprofileForm(instance=userprofile)
    context = {
        'user_form': user_form,
        'profile_form': profile_form,
        'userprofile': userprofile,
    }
    return render(request, 'accounts/edit_profile.html', context)









@login_required(login_url='login')
def changepassword(request):
    if request.method == 'POST':
        current_password = request.POST['current_password']
        new_password = request.POST['new_password']
        confirm_password = request.POST['confirm_password']

        user = Account.objects.get(username__exact=request.user.username)

        if new_password == confirm_password:
            success = user.check_password(current_password)
            if success:
                user.set_password(new_password)
                user.save()
                # auth.logout(request)
                messages.success(request, 'Password updated successfully.')
                return redirect('changepassword')
            else:
                messages.error(request, 'Please enter valid current password')
                return redirect('changepassword')
        else:
            messages.error(request, 'Password does not match!')
            return redirect('changepassword')
    return render(request, 'accounts/change_password.html')


@login_required(login_url='login')
def profile(request):
    current_user = request.user.username
    logged_in_user = request.user.username
    user_followers = len(FollowersCount.objects.filter(user=current_user))
    user_following = len(FollowersCount.objects.filter(follower=current_user))
    user_followers0 = FollowersCount.objects.filter(user = current_user)
    user_followers1 = []

    for i in user_followers0:
        user_followers0 = i.follower
        user_followers1.append(user_followers0)
    if logged_in_user in user_followers1:
        follow_button_value = 'unfollow'
    else:
        follow_button_value = 'follow'
    # userprofile = Userprofile.objects.get(user_id=request.user.id)
    post = Post.objects.all()
    context = {
        # 'userprofile' : userprofile,
        'posts' :  post,
        'current_user' : current_user,
        'user_followers' : user_followers,
        'user_following' : user_following,
        'follow_button_value' : follow_button_value

    }
    return render(request, 'accounts/profile.html',context)



def followers_count(request):
   if request.method == 'POST':
       value = request.POST['value']
       user = request.POST['user']
       follower = request.POST['follower']
       if value == 'follow':
           followers_cnt = FollowersCount.objects.create(follower=follower, user=user)
           followers_cnt.save()
       else:
           followers_cnt = FollowersCount.objects.get(follower=follower, user=user)
           followers_cnt.delete()

       return redirect('/?user=' + user)