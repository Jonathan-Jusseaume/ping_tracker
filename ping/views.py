from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect, render

# Create your views here.
from ping.models import Match, Note, Opponent, UserStats


def login_view(request):
    if request.user.is_anonymous:
        return render(request, "login/login.html")
    return redirect("/dashboard")


def logout_view(request):
    logout(request)
    return redirect("/dashboard")


def check_connexion(request):
    username = request.POST.get('login', False)
    password = request.POST.get('password', False)
    user = authenticate(username=username, password=password)
    if user is not None and user.is_active:
        login(request, user)
        return redirect("/dashboard")
    return render(request, "login/login.html", {"error": 1})


def main(request):
    if request.user.is_anonymous:
        return redirect("/")
    my_user_stats = UserStats.objects.get_or_create(user=request.user)[0]
    return render(request, "dashboard/dashboard.html",
                  {"win_lose_ratio": my_user_stats.get_win_lose_ratio(),
                   "fifth_set_ratio": my_user_stats.get_fifth_set_ratio(),
                   "clutch_set_ratio": my_user_stats.get_clutch_set_ratio(),
                   "average_opponents": my_user_stats.get_average_opponents()})


def notes(request):
    if request.user.is_anonymous:
        return redirect("/")
    return render(request, "notes/notes.html", {"notes": Note.get_notes_of_user(request.user)})


def history(request):
    if request.user.is_anonymous:
        return redirect("/")
    return render(request, "history/history.html", {"matchs": Match.get_matchs_of_user(request.user)})


def match(request):
    if request.user.is_anonymous:
        return redirect("/")
    return render(request, "add-match/add-match.html", {"opponents": list(Opponent.objects.all())})


def submit_match(request):
    if request.user.is_anonymous:
        return redirect("/")
    if request.method == 'POST':
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
        Match.add_match(request.user,
                        opponent,
                        user_scores,
                        opponent_scores,
                        request.POST.get("comment"),
                        request.POST.get("date"),
                        request.POST.get("rank"))
    return redirect("/historique")


def add_notes(request):
    if request.user.is_anonymous:
        return redirect("/")
    if request.method == 'POST':
        note = request.POST.get('note')
        if note is not None:
            Note.add_note(request.user, note)
    return redirect("/notes")
