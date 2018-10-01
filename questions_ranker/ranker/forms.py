from django import forms

from .models import (
    Question,
    Ranking,
    RankingEntry,
)


class RankingEntryForm(forms.ModelForm):
    class Meta:
        fields = ('rank', )
        model = RankingEntry
        widgets = {
            'rank': forms.RadioSelect(),
        }
