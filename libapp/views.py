from django.core.urlresolvers import reverse
from django.shortcuts import render
# Create your views here.
# Import necessary classes
from django.http import HttpResponse
from django.core import serializers
from libapp.forms import SuggestionForm, SearchlibForm, LoginForm, LibuserForm
from libapp.models import Book, Dvd, Libuser, Libitem, Suggestion
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
import operator

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test

# Create your viewsx     here.
def searchlib(request):
    if request.method == 'POST':
        SearchlibForm(request.POST)
        title1 = request.POST['title']
        author1 = request.POST['author']
        if title1 != '' and author1 != '':  # Title and User not null
            bookob = Book.objects.filter(title__contains=title1, author__contains=author1)
            dvdob = Dvd.objects.filter(title__contains=title1, maker__contains=author1)
            form = SearchlibForm()
            if bookob and dvdob:
                return render(request, 'libapp/searchitem.html', {'bookob': bookob, 'dvdob': dvdob, 'form': form})
            elif not bookob and dvdob:
                return render(request, 'libapp/searchitem.html', {'dvdob': dvdob, 'form': form})
            elif bookob and not dvdob:
                return render(request, 'libapp/searchitem.html', {'bookob': bookob, 'form': form})
            else:
                return render(request, 'libapp/searchitem.html', {'notfound': True, 'form': form})

        elif title1 != '' and author1 == '':  # Only Title searched
            bookob = Book.objects.filter(title__contains=title1)
            dvdob = Dvd.objects.filter(title__contains=title1)
            form = SearchlibForm()
            if bookob and dvdob:
                return render(request, 'libapp/searchitem.html', {'bookob': bookob, 'dvdob': dvdob, 'form': form})
            elif bookob and not dvdob:
                return render(request, 'libapp/searchitem.html', {'bookob': bookob, 'form': form})
            elif not bookob and dvdob:
                return render(request, 'libapp/searchitem.html', {'dvdob': dvdob, 'form': form})
            else:
                return render(request, 'libapp/searchitem.html', {'notfound': True, 'form': form})

        elif author1 != '' and title1 == '':  # Only Author searched
            bookob = Book.objects.filter(author__contains=author1)
            dvdob = Dvd.objects.filter(maker__contains=author1)
            form = SearchlibForm()
            if bookob and dvdob:
                return render(request, 'libapp/searchitem.html', {'bookob': bookob, 'dvdob': dvdob, 'form': form})
            elif bookob and not dvdob:
                return render(request, 'libapp/searchitem.html', {'bookob': bookob, 'form': form})
            elif not dvdob and bookob:
                return render(request, 'libapp/searchitem.html', {'dvdob': dvdob, 'form': form})
            else:
                form = SearchlibForm()
                return render(request, 'libapp/searchitem.html', {'notfound': True, 'form': form})

        else:  # Author and Title null
            form = SearchlibForm()
            return render(request, 'libapp/searchitem.html', {'notinput': True, 'form': form})

    else:
        form = SearchlibForm()
        return render(request, 'libapp/searchitem.html', {'form': form})





def newitem1(request):
    return  render(request,'libapp/newitem.html')

def suggestions(request):
    suggestionlist = Suggestion.objects.all()[:10]
    return render(request, 'libapp/suggestions.html', {'itemlist':   suggestionlist})


def detail(request,item_id):
    item = Libitem.objects.get(pk=item_id)
    if item.itemtype == 'Book':
        item = Book.objects.get(pk=item_id)
    else:
        item = Dvd.objects.get(pk=item_id)
    return render(request, 'libapp/detail.html', {'item': item})

def suggestiondetail(request,item_id):
    item = Suggestion.objects.get(pk=item_id)
    return render(request, 'libapp/suggestiondetail.html', {'item': item})

def detail1(request, item_id):
    response = HttpResponse()
    type='Book'
    try:
        item = Book.objects.get(pk=item_id)
        para3 = '<p>Author: ' + str(item.author) + '</p>'
    except Book.DoesNotExist:  # catch the DoesNotExist error
        # item = Dvd.objects.get(pk=item_id)
        item = get_object_or_404(Dvd, pk=item_id)
        type = 'Dvd'
        para3 = '<p>Maker: ' + str(item.maker) + '</p>'

    para = '<p>This is a ' + type + '</p>'
    para1 = '<p>Title: ' + item.title + '</p>'
    para2 = '<p>Due Date: ' + str(item.duedate) + '</p>'
    response.write(para)
    response.write(para1)
    response.write(para2)
    response.write(para3)

    return response

def index(request):
    itemlist = Libitem.objects.all().order_by('title')[:10]
    try:
        request.session['luckynum']
        request.session['model_pic']
    except KeyError:
        request.session['luckynum'] = 0;
        request.session['model_pic'] = 0;
    return render(request, 'libapp/index.html', {'itemlist': itemlist, 'luckynum': request.session['luckynum'], 'model_pic' :request.session['model_pic']})


def index1(request):
    booklist = Book.objects.all() [:10]
    response = HttpResponse()
    heading1 = '<p>' + 'List of books: ' + '</p>'
    response.write(heading1)
    for book in booklist:
        para = '<p>' + str(book) + '</p>'
        response.write(para)

    dvdlist = Dvd.objects.all().order_by('pubyr') [:5]
    heading2 = '<p>' + 'List of dvds: ' + '</p>'
    response.write(heading2)
    for dvd in dvdlist:
        para1 = '<p>' + str(dvd) + '</p>'
        response.write(para1)
    return response


def about(request):
    try:
        request.session['about_visits'] += 1
    except KeyError:
        request.session.set_expiry(300)
        request.session['about_visits'] = 0;
    return render(request, 'libapp/about.html', {'about_visits': request.session['about_visits']})

def about1(request):
    response =  HttpResponse()
    heading1 = '<p>' + 'This is a Library APP.' + '</p>'
    response.write(heading1)
    return response

import random

def user_login(request):
    form = LoginForm()
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None and user.is_active:
            request.session.set_expiry(3600)
            n = random.randint(1, 9)
            request.session['luckynum'] = n;
            login(request, user)
            userob = Libuser.objects.filter(username=request.user.username)
            value = 'pic_folder/download.jpg'
            # if userob.length > 0:
            if userob:
                if str(userob[0].model_pic):
                    if str(userob[0].model_pic) != 'pic_folder/None/no-img.jpg':
                        value = str(userob[0].model_pic)[14:]
            request.session['model_pic'] = value
            request.session['userob'] = serializers.serialize('json', userob)


            return HttpResponseRedirect('http://127.0.0.1:8000/libapp/')
        elif user is None:
            return render(request, 'libapp/login.html', {'notlogin': True, 'form': form})
        else:
            return render(request, 'libapp/login.html', {'notactive': True, 'form': form})
    else:
        return render(request, 'libapp/login.html', {'form': form})

@login_required
def user_logout(request):
    logout(request)
    # return HttpResponseRedirect(reverse(('libapp:index')))
    return HttpResponseRedirect('http://127.0.0.1:8000/libapp/')

from django.contrib.auth.hashers import make_password

def register(request):
    libuser = Libuser.objects.all()
    if request.method == 'POST':
        form = LibuserForm(request.POST)
        if form.is_valid():
            libuser = form.save(commit=False)
            libuser.num_interested = 1
            libuser.password = make_password(form.cleaned_data['password'])
            libuser.save()
            return HttpResponseRedirect('http://127.0.0.1:8000/libapp/login/')
        else:
            return render(request, 'libapp/register.html', {'form':form})
    else:
        form = LibuserForm()
        return render(request, 'libapp/register.html', {'form':form})

def newitem(request):
    suggestions = Suggestion.objects.all()
    if request.method == 'POST':
        form = SuggestionForm(request.POST)
        if form.is_valid():
            suggestion = form.save(commit=False)
            suggestion.num_interested = 1
            suggestion.save()
            return HttpResponseRedirect('/libapp/suggestions/')
        else:
            return render(request, 'libapp/newitem.html', {'form':form, 'suggestions':suggestions})
    else:
        form = SuggestionForm()
        return render(request, 'libapp/newitem.html', {'form':form, 'suggestions':suggestions})

def myacct(request):
    userob = Libuser.objects.get(id=request.user.id)
    d = {'first_name': userob.first_name, 'last_name': userob.last_name, 'emailid': userob.email,
         'address': userob.address, 'city': userob.city, 'province': userob.province, 'phone': userob.phone}
    if request.method == 'POST':
        userob = Libuser.objects.filter(id=request.user.id).update(
            first_name=request.POST['first_name'],
            last_name=request.POST['last_name'],
            email=request.POST['emailid'],
            address=request.POST['address'],
            city=request.POST['city'],
            province=request.POST['province'],
            phone=request.POST['phone']
        )
        userob = Libuser.objects.get(id=request.user.id)
        d = {'first_name': userob.first_name, 'last_name': userob.last_name, 'emailid': userob.email,
             'address': userob.address, 'city': userob.city, 'privince': userob.province, 'phone': userob.phone}
        d1 = 'True'
        return render(request, 'libapp/myacct.html', {"values": d, "record_added": d1})
    else:
        return render(request, 'libapp/myacct.html', {"values": d})

def myitems(request):
    itemob = Libitem.objects.filter(user__username=request.user.username, checked_out=True)
    return render(request, 'libapp/myitem.html', {'itemob': itemob})
