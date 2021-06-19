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

def update(request, id):
    errors = Book.objects.basic_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect(f"/was_favorited_check/{id}")
    else:
        clicked_book = Book.objects.get(id=id)
        clicked_book.title=request.POST['title']
        clicked_book.description=request.POST['description']
        clicked_book.save()
        messages.success(request, "Favorite book successfully updated")
        return redirect("/books")

def books_all(request, id):
    if 'user_id' not in request.session:
        return redirect('/')
    this_user = User.objects.filter(id = request.session['user_id'])
    clicked_book = Book.objects.get(id=id)
    book_likers = clicked_book.users.all()
    context = {
        "current_user" : this_user[0], 
        "all_books": Book.objects.all(),
        "clicked_book": clicked_book,
        "book_likers": book_likers,
        }
    return render(request, "view_book.html", context)

def add_favorite_book(request, id):
    if 'user_id' not in request.session:
        return redirect('/')
    this_user = User.objects.filter(id = request.session['user_id'])
    clicked_book = Book.objects.get(id=id) #getting clicked book
    #need to add book to User's liked books
    clicked_book.users.add(this_user[0])
    return redirect('/books')

def was_favorited_check(request, id):
    if 'user_id' not in request.session:
        return redirect('/')
    this_user = User.objects.filter(id = request.session['user_id'])
    clicked_book = Book.objects.get(id=id)
    book_likers = clicked_book.users.all()
    all_books= Book.objects.all()
    current_user = this_user[0]
    # for book in all_books:
    if current_user.id == clicked_book.upload_status.id:
        context = {
            "current_user" : this_user[0], 
            "book_likers": book_likers,
            "clicked_book": Book.objects.get(id=id),
        }
        return render (request, "edit_book.html", context)
#if uploaded, show edit form:
    else:
        context = {
            "current_user" : this_user[0], 
            "book_likers": book_likers,
            "clicked_book": Book.objects.get(id=id),
        }
        return redirect (f"/books/{id}")

def delete(request, id):
    if 'user_id' not in request.session:
        return redirect('/')
    clicked_book = Book.objects.get(id=id)
    this_user = User.objects.filter(id = request.session['user_id'])
    current_user = this_user[0]
    if current_user.id != clicked_book.upload_status.id:
        return redirect('/')
    d = Book.objects.get(id=id)
    d.delete()
    return redirect('/books')

def unfavorite(request, id):
    if 'user_id' not in request.session:
        return redirect('/')
    this_user = User.objects.filter(id = request.session['user_id'])
    clicked_book = Book.objects.get(id=id) #getting clicked book
    clicked_book.users.remove(this_user[0])
    return redirect('/books')
