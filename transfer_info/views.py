from django.shortcuts import render
from django.http import HttpResponse

from .models import Movies

import requests

from .database import Database

import json
# Create your views here.

def result(request):
    # accept data from client
    if request.method == 'POST':
        Database.populatedb(request.body.decode("utf-8"))

    # add data to the database 
    try:
        member_list = Movies.objects.all()
    except Movies.DoesNotExist:
         raise Http404("Nothing in the database")


    to_take_movies: json
    to_take_movies = Database.best_movie()
    to_take_movies.append({"Total": len(Database.best_movie())})
    payload = json.dumps(to_take_movies)

    return HttpResponse(payload)