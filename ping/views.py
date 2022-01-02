from django.shortcuts import redirect, render

# Create your views here.
from ping.models import Match, Note, Set


def main(request):
    return render(request, "dashboard/dashboard.html",
                  {"win_lose_ratio": Match.get_win_lose_ratio(request.user),
                   "fifth_set_ratio": Set.get_fifth_set_ratio(request.user),
                   "clutch_set_ratio": Set.get_clutch_set_ratio(request.user)})


def notes(request):
    return render(request, "notes/notes.html", {"notes": Note.get_notes_of_user(request.user)})


def history(request):
    return render(request, "history/history.html", {"matchs": Match.get_matchs_of_user(request.user)})


def add_notes(request):
    if request.method == 'POST':
        note = request.POST.get('note')
        if note is not None:
            Note.add_note(note)
    return redirect("/notes")
