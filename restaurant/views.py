from django.shortcuts import render,redirect
from .forms import BookingForm
from .models import Menu
from django. contrib import messages
from django.contrib.auth.models import User, auth

# Create your views here.

def home(request):
    return render(request, 'index.html')

def about(request):
    return render(request, 'about.html')

def book(request):
    form = BookingForm()
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            form.save()
            #extra
            messages.success(request, 'Your table is booked.Thank You!!')
            return render(request, 'book.html', {'form': BookingForm(request.GET)})
        else:
            messages.error(request, 'Invalid form submission.') #extraa
    else: #extraaa
        context = {'form':form}
        return render(request, 'book.html', context)


def menu(request):
    menu_data = Menu.objects.all().order_by('name')
    main_data = {"menu": menu_data}
    return render(request, 'menu.html', {"menu": main_data})


def display_menu_item(request, pk=None): 
    if pk: 
        menu_item = Menu.objects.get(pk=pk) 
    else: 
        menu_item = "" 
    return render(request, 'menu_item.html', {"menu_item": menu_item}) 

def login(request):
    if request.method =='POST':
        username = request.POST['username']
        password = request.POST['password']

        user=auth.authenticate(username=username,password=password)

        if user is not None:
            auth.login(request,user) 
            return redirect("/")
        else:
            messages.info(request,"Invalid credentials...")
            return redirect('login')

    else:
        return render(request,'login.html')
    

def register(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        password1 = request.POST['password1']
        password2  = request.POST['password2']
        email = request.POST['email']
        
        if password1==password2:
            if User.objects.filter(username=username) or User.objects.filter(email=email).exists():
                messages.info(request,'Either Username or email already taken...')
                return redirect('register')
             
            else:
                user=User.objects.create_user(username=username, password=password1,email=email,first_name=first_name,last_name=last_name)
                user.save();
                print('User created')
                return redirect('login')
        else:
            messages.info(request,'Password not mathcing...')
            return redirect('register')
        
        return redirect('')

    else:
        return render(request,'register.html')
    

    
def logout(request):
    auth.logout(request)
    return redirect("/")