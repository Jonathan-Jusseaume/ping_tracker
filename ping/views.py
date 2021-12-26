import json

from django.shortcuts import render

# Create your views here.
from ping.models import *


def main(request):
    win_lose_ratio = {
        'Victoire': Match.objects.filter(status__id=StatusType.VICTORY.value).count(),
        'Défaite': Match.objects.filter(status__id=StatusType.DEFEAT.value).count()
    }
    print(json.dumps(win_lose_ratio))

    return render(request, "dashboard/dashboard.html", {"win_lose_ratio": win_lose_ratio})


def notes(request):
    return render(request, "notes/notes.html")


def history(request):
    print(request.user)
    matchs = Match.objects.all()
    for match in matchs:
        match.get_sets_of_match()
    return render(request, "history/history.html", {"matchs": matchs})
