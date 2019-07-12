from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from .models import *
import random, datetime

def index(request): #Redirect
    return redirect('/shows')

def shows(request): #Render MAIN PAGE
    context = {
        'Shows': Shows.objects.all()

    }
    return render(request, 'SHOWS/index.html', context)

def newShow(request): #Render FOR NEW SHOW
    context = {

    }
    return render(request, 'SHOWS/newshow.html', context)

def newShowProcess(request): #Process FOR NEW SHOW
    
    errors = Shows.objects.validator(request.POST)

    if len(errors) > 0:
        for tags, value in errors.items():
            print('*'*50, '\n', 'processing', '\n', '*'*50)
            messages.error(request, value)
        return redirect('/shows/new')

    else:
        title = request.POST['title']
        network = request.POST['network']
        release = request.POST['release']
        description = request.POST['description']
        if title != '':
            newShow = Shows.objects.create(title=title, network=network, description=description, release_date=release)
        messages.success(request, "Successfully added")
        return redirect('/shows/details/%s' % (newShow.id))

def showDetails(request, showID): #Render FOR DETAILS
    context = {
        'thisShow': Shows.objects.get(id= showID)

    }

    return render(request, 'SHOWS/details.html', context)

def showEdit(request, showID): #Render FOR SHOW EDIT
    context = {
        'thisShow': Shows.objects.get(id= showID)
    }
    return render(request, 'SHOWS/edit.html', context)

def showEditProcess(request, showID): #Process FOR SHOW EDIT

    errors = Shows.objects.validator(request.POST)

    if len(errors) > 0:
        for tags, value in errors.items():
            print('*'*50, '\n', 'processing', '\n', '*'*50)
            messages.error(request, value)
        return redirect('/shows/details/%s/edit' % (showID))
    else:
        thisShow = Shows.objects.get(id= showID)
        thisShow.title = request.POST['title']  or thisShow.title
        thisShow.network = request.POST['network']  or thisShow.network
        thisShow.release_date = request.POST['release']  or thisShow.release_date
        thisShow.description = request.POST['description']  or thisShow.description
        thisShow.save()
        return redirect('/shows/details/%s' % (showID))

def showDelete(request, showID): #Process for Delete
    thisShow = Shows.objects.get(id= showID)
    thisShow.delete()
    return redirect('/shows')
