from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from .models import *

def index(request):
    return render(request, "login.html")

def check_registration(request):
    errors = User.objects.basic_validator(request.POST)
    email = request.POST['email']
    if request.method == "GET":
        return redirect('/')
    elif len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')
    #changed to check len of dictionary
    elif len(User.objects.filter(email=email)) >= 1:
        messages.error(request, "Email is already in use")
        return redirect('/')
    else:
        hashed_pw = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()).decode()
        new_user = User.objects.create(first_name = request.POST['first-name'], last_name = request.POST['last-name'], email = request.POST['email'], password = hashed_pw)
        request.session['user_id'] = new_user.id
        return redirect('/books')

def check_login(request):
    if request.method == "GET":
        return redirect ("/")
    else:
        errors = User.objects.login_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/')
        this_user = User.objects.filter(email=request.POST['email'])
        request.session['user_id'] = this_user[0].id
        return redirect('/books')

def check_book(request):
    if request.method == "GET":
        return redirect ("/books") #add id parameter
    else:
        errors = Book.objects.basic_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/books')
        #if no issues, create a book
        this_user = User.objects.get(id = request.session['user_id'])
        Book.objects.create(title=request.POST['title'], description=request.POST['description'], upload_status=this_user)
        new_book = Book.objects.last() #might need to refine this, change to get request.session
        new_book.users.add(this_user)
        return redirect("/books") 

def books(request):
    if 'user_id' not in request.session:
        return redirect('/')
    this_user = User.objects.filter(id = request.session['user_id'])
    context = {
        "current_user" : this_user[0], #grabs from session rather than database to prevent refreshing into login
        "all_books": Book.objects.all(),
        }
    return render(request, "add_book.html", context)

def logout(request):
    request.session.flush()
    return redirect('/')

def update(request):
    return render(request, "edit_book.html")

def all(request, id):
    if 'user_id' not in request.session:
        return redirect('/')
    this_user = User.objects.filter(id = request.session['user_id'])
    context = {
        "current_user" : this_user[0], #grabs from session rather than database to prevent refreshing into login
        "current_book": Book.objects.last(),
        "all_books": Book.objects.all(),
        }
    return render(request, "view_book.html", context)