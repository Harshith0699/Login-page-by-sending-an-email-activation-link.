from django.shortcuts import redirect, render

# Create your views here.
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.core.mail import send_mail
from mysite import settings

def hello_world(request):
    return render(request,'myapp/index.html')

def signin(request):
    if request.method == 'POST':
        username = request.POST['username']
        pass1 = request.POST['pass1'] 
        user = authenticate(username=username,password=pass1)
        if user is not None:
            login(request,user)
            f_name=user.first_name
            return render(request,"myapp/index.html",{'f_name':f_name})
        else:
            messages.error(request,"Wrong credentials")
        return redirect('hello_world')

        
    return render(request,'myapp/signin.html')

def signout(request):
    logout(request)
    messages.success(request,"Logged out")
    return redirect('hello_world')

def signup(request):
    if request.method == 'POST':
        username = request.POST['user']
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']

        if User.objects.filter(username=username):
            messages.error(request,"username already present")
            return redirect('hello_world')
        if User.objects.filter(email=email):
            messages.error(request,"email already present")
            return redirect('hello_world')
        

        myuser = User.objects.create_user(username,email,pass1)
        myuser.first_name = fname
        myuser.last_name= lname
        myuser.save()
        messages.success(request,"Your account has been created successfully")

        subject='Welcome Django'
        message="hello, welcome email"
        from_email = settings.EMAIL_HOST_USER
        to_email=[myuser.email]
        send_mail(subject,message,from_email,to_email,fail_silently=True)

        return redirect('signin')

    return render(request, 'myapp/signup.html')

