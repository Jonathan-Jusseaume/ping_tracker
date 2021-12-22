from django.shortcuts import render

# Create your views here.
from ping.models import *


def main(request):
    return render(request, "main.html")


def notes(request):
    return render(request, "notes/notes.html")


def history(request):
    print(request.user)
    matchs = Match.objects.all()
    for match in matchs:
        match.get_sets_of_match()
    return render(request, "history/history.html", {"matchs": matchs})
