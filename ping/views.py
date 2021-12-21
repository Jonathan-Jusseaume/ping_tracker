from django.shortcuts import render


# Create your views here.
def main(request):
    return render(request, "main.html")


def notes(request):
    return render(request, "notes/notes.html")


def history(request):
    return render(request, "history/history.html")
