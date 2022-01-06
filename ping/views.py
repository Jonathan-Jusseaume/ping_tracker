from django.shortcuts import redirect, render

# Create your views here.
from ping.models import Match, Note, Opponent, Set


def main(request):
    return render(request, "dashboard/dashboard.html",
                  {"win_lose_ratio": Match.get_win_lose_ratio(request.user),
                   "fifth_set_ratio": Set.get_fifth_set_ratio(request.user),
                   "clutch_set_ratio": Set.get_clutch_set_ratio(request.user)})


def notes(request):
    return render(request, "notes/notes.html", {"notes": Note.get_notes_of_user(request.user)})


def history(request):
    return render(request, "history/history.html", {"matchs": Match.get_matchs_of_user(request.user)})


def match(request):
    return render(request, "add-match/add-match.html", {"opponents": list(Opponent.objects.all())})


def submit_match(request):
    if request.method == 'POST':
        print(request.POST)
        opponent = Opponent.insert(request.POST.get("id_license"),
                                   request.POST.get("last_name"),
                                   request.POST.get("first_name"))
        user_scores = [request.POST.get("user_1"),
                       request.POST.get("user_2"),
                       request.POST.get("user_3"),
                       request.POST.get("user_4"),
                       request.POST.get("user_5")]
        opponent_scores = [request.POST.get("opponent_1"),
                           request.POST.get("opponent_2"),
                           request.POST.get("opponent_3"),
                           request.POST.get("opponent_4"),
                           request.POST.get("opponent_5")]
        user_scores = list(filter(lambda user_score: user_score != "", user_scores))
        opponent_scores = list(filter(lambda opponent_score: opponent_score != "", opponent_scores))
        Match.add_match(opponent,
                        user_scores,
                        opponent_scores,
                        request.POST.get("comment"),
                        request.POST.get("date"),
                        request.POST.get("rank"))
    return redirect("/historique")


def add_notes(request):
    if request.method == 'POST':
        note = request.POST.get('note')
        if note is not None:
            Note.add_note(note)
    return redirect("/notes")
