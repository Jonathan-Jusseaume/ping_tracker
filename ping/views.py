from django.shortcuts import render

# Create your views here.
from ping.models import *


def main(request):
    return render(request, "dashboard/dashboard.html",
                  {"win_lose_ratio": Match.get_win_lose_ratio(request.user),
                   "fifth_set_ratio": Set.get_fifth_set_ratio(request.user),
                   "clutch_set_ratio": Set.get_clutch_set_ratio(request.user)})


def notes(request):
    return render(request, "notes/notes.html")


def history(request):
    print(request.user)

    return render(request, "history/history.html", {"matchs": Match.get_matchs_of_user(request.user)})
