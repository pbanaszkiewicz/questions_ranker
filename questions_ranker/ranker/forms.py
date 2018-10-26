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
    def __init__(self, submit_name='submit', submit_label=_("Save")):
        super().__init__()
        self.form_class = 'form-horizontal'
        self.label_class = 'col-lg-2'
        self.field_class = 'col-lg-10'
        self.add_input(Submit(submit_name, submit_label))


class Bootstrap4HelperNonHorizontal(FormHelper):
    def __init__(self, submit_name='submit', submit_label=_("Save")):
        super().__init__()
        self.form_class = ''
        self.label_class = ''
        self.field_class = ''
        self.add_input(Submit(submit_name, submit_label))


class RankingEntryForm(forms.ModelForm):
    class Meta:
        fields = ('rank', )
        model = RankingEntry
        widgets = {
            'rank': forms.RadioSelect(),
        }


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


class RankingDemographicForm(forms.ModelForm):
    helper = Bootstrap4HelperNonHorizontal()

    class Meta:
        fields = (
            'teaching_children_in_schools',
            'teaching_teens_in_schools',
            'teaching_students',
            'teaching_adults',
            'teaching_children_free_range',
            'teaching_teens_free_range',
            'teaching_adults_free_range',
            'daily_home_computer',
            'daily_school_computer',
            'daily_smartphone',
            'daily_broadband',
            'daily_lowspeed',
            'comp_research_involvement',
        )
        model = Ranking
        widgets = {
            'teaching_children_in_schools': forms.RadioSelect(),
            'teaching_teens_in_schools': forms.RadioSelect(),
            'teaching_students': forms.RadioSelect(),
            'teaching_adults': forms.RadioSelect(),
            'teaching_children_free_range': forms.RadioSelect(),
            'teaching_teens_free_range': forms.RadioSelect(),
            'teaching_adults_free_range': forms.RadioSelect(),
            'daily_home_computer': forms.RadioSelect(),
            'daily_school_computer': forms.RadioSelect(),
            'daily_smartphone': forms.RadioSelect(),
            'daily_broadband': forms.RadioSelect(),
            'daily_lowspeed': forms.RadioSelect(),
            'comp_research_involvement': forms.RadioSelect(),
        }
