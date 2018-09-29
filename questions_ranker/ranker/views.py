from django.shortcuts import render, get_object_or_404

from .models import (
    Question,
    Ranking,
)


def home(request):
    """Display home view with information about this research."""
    return render(request, "pages/home.html")


def rank(request, hash_id):
    """Display questionnaire form; keep track of attempts via session."""
    ranking = get_object_or_404(Ranking, hash_id=hash_id)
    return render(request, "pages/home.html", {'additional_text': hash_id})
