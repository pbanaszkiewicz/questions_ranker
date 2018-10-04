from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

from .models import (
    Question,
    Ranking,
    RankingEntry,
    DrawEntry,
)


class Bootstrap4Helper(FormHelper):
    form_class = 'form-horizontal'
    label_class = 'col-lg-2'
    field_class = 'col-lg-10'

    def __init__(self, submit_name='submit', submit_label=_("Save")):
        super().__init__()
        self.add_input(Submit(submit_name, submit_label))


class RankingEntryForm(forms.ModelForm):
    class Meta:
        fields = ('rank', )
        model = RankingEntry
        widgets = {
            'rank': forms.RadioSelect(),
        }


class RankingGeoForm(forms.ModelForm):
    helper = Bootstrap4Helper()

    class Meta:
        fields = ('rank', )
        model = RankingEntry


class DrawEntryForm(forms.ModelForm):
    helper = Bootstrap4Helper()

    class Meta:
        fields = ('email', 'draw', 'paper')
        model = DrawEntry
        widgets = {
            'draw': forms.RadioSelect(),
            'paper': forms.RadioSelect(),
        }

    def clean_draw(self):
        draw = self.cleaned_data['draw']
        email = self.cleaned_data['email']
        if draw is True and not email:
            raise ValidationError(_("No e-mail provided."))
        return draw

    def clean_paper(self):
        paper = self.cleaned_data['paper']
        email = self.cleaned_data['email']
        if paper is True and not email:
            raise ValidationError(_("No e-mail provided."))
        return paper
