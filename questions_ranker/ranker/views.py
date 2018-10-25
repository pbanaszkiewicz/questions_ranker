from django.contrib import messages
from django.forms import modelformset_factory
from django.http import Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.utils.translation import ugettext as _

from .models import (
    Category,
    Question,
    Ranking,
    RankingEntry,
)

from .forms import (
    RankingEntryForm,
    DrawEntryForm,
    RankingDemographicForm,
)


def home(request):
    """Display home view with information about this research."""
    return render(request, "pages/home.html")


def rank_start(request, hash_id):
    """Generate questions for the ranking; show [start] button.
    If the ranking is complete, show the thank-you page."""
    ranking = get_object_or_404(
        Ranking.objects.prefetch_related('entries'),
        hash_id=hash_id,
    )

    # if ranking stage is >=4, show the "thank you" page
    if ranking.stage >= 4:
        context = {
            'title': _("Thank you for participation"),
            'page_header': _("Thank you!"),
        }
        return render(request, "ranker/thankyou.html", context)

    elif ranking.stage > 0:
        next_stage = ranking.stage + 1
        return redirect(reverse('rank_stage',
                                args=[hash_id, next_stage]))

    if not ranking.category_stage1 or not ranking.category_stage2:
        # generate categories and questions
        # make sure there are selected categories for both stages
        categories_used_pk = []
        if ranking.category_stage1:
            categories_used_pk.append(ranking.category_stage1.pk)
        if ranking.category_stage2:
            categories_used_pk.append(ranking.category_stage2.pk)

        if len(categories_used_pk) < 2:
            categories_pk = Category.objects.exclude(pk__in=categories_used_pk) \
                                            .values_list('pk', flat=True) \
                                            .order_by('?')
            categories_iter = iter(categories_pk)

            try:
                if not ranking.category_stage1:
                    ranking.category_stage1 = Category.objects.get(
                        pk=next(categories_iter)
                    )

                    # save questions within the ranking as well
                    questions = Question.objects.filter(
                        category=ranking.category_stage1,
                        active=True,
                    ).order_by('?')

                    # create an M2M link (through-table entry)
                    RankingEntry.objects.bulk_create([
                        RankingEntry(
                            ranking=ranking,
                            question=question,
                            rank=None,
                            stage=2,
                        )
                        for question in questions
                    ])

                if not ranking.category_stage2:
                    ranking.category_stage2 = Category.objects.get(
                        pk=next(categories_iter)
                    )

                    # save questions within the ranking as well
                    questions = Question.objects.filter(
                        category=ranking.category_stage2,
                        active=True,
                    ).order_by('?')

                    # create an M2M link (through-table entry)
                    RankingEntry.objects.bulk_create([
                        RankingEntry(
                            ranking=ranking,
                            question=question,
                            rank=None,
                            stage=3,
                        )
                        for question in questions
                    ])

                ranking.save()

            except StopIteration:
                raise Http404("Not enough categories to choose from.")

    # show [start] button page
    context = {
        'title': _("Questions for Computing Education Researchers"),
        'hash_id': hash_id,
        'page_header': _("Survey"),
    }
    return render(request, "ranker/start.html", context)


def rank_email(request, hash_id):
    """Display draw entry form, save potential email address in the database."""
    stage = 1
    ranking = get_object_or_404(
        Ranking,
        hash_id=hash_id,
        stage=stage - 1,
    )

    if request.method == "POST":
        form = DrawEntryForm(request.POST)

        if form.is_valid():
            # accept user entry
            obj = form.save()
            # increment stage in ranking
            ranking.stage = stage
            ranking.save()

            messages.success(
                request,
                _("Thank you for getting started - the following pages list "
                  "the questions we would like you to prioritize."),
            )

            return redirect(
                reverse('rank_stage', args=[hash_id, stage + 1]),
            )

        else:
            messages.error(request, _("Fix errors in the form below."),
                           extra_tags="danger")

    else:
        form = DrawEntryForm()

    page_header = _("Page {} of 4").format(1)
    questions_num = ranking.entries.count()
    categories_num = 2

    context = {
        'title': _("Questions for Computing Education Researchers"),
        'hash_id': hash_id,
        'form': form,
        'page_header': page_header,
        'questions_num': questions_num,
        'categories_num': categories_num,
    }

    return render(request, "ranker/email.html", context)


def rank_demographic(request, hash_id):
    """Display demographic questions form, save as part of ranking entry object."""
    stage = 4
    ranking = get_object_or_404(
        Ranking,
        hash_id=hash_id,
        stage=stage - 1,
    )

    if request.method == "POST":
        form = RankingDemographicForm(request.POST, instance=ranking)

        if form.is_valid():
            # accept user entry
            obj = form.save()
            # increment stage in ranking
            obj.stage = stage
            obj.save()

            messages.success(request,
                             _("Thank you for completing last stage of the ranking."))

            return redirect(
                reverse('rank_stage', args=[hash_id, stage + 1]),
            )

        else:
            messages.error(request, _("Please answer all questions."),
                           extra_tags="danger")

    else:
        form = RankingDemographicForm(instance=ranking)

    page_header = _("Page {} of 4").format(4)

    context = {
        'title': _("Questions for Computing Education Researchers"),
        'hash_id': hash_id,
        'form': form,
        'page_header': page_header,
    }

    return render(request, "ranker/demographic.html", context)


def rank_stage(request, hash_id, stage):
    """Show questionnaire for selected stage; validate stage number."""
    try:
        stage = int(stage)
    except (TypeError, ValueError):
        raise Http404("Unable to parse `stage` from URL.")

    # ensure correct stage value
    # this view accepts only 2 and 3
    if stage < 1 or stage > 4:
        return redirect(reverse('rank_start', args=[hash_id]))
    elif stage == 1:
        return redirect(reverse('rank_email', args=[hash_id]))
    elif stage == 4:
        return redirect(reverse('rank_demographic', args=[hash_id]))

    ranking = get_object_or_404(
        Ranking.objects.prefetch_related('entries'),
        hash_id=hash_id,
        stage=stage - 1,
    )

    entries_stage = (
        ranking.rankingentry_set
            .filter(stage=ranking.stage + 1)
            .select_related('question', 'question__category')
    )

    # build a Formset with initial questions
    RankingEntryFormset = modelformset_factory(
        RankingEntry,
        form=RankingEntryForm,
        extra=0, max_num=0,
    )

    if request.method == "POST":
        formset = RankingEntryFormset(request.POST, queryset=entries_stage)

        if formset.is_valid():
            # accept user entries
            formset.save()
            # update ranking stage
            ranking.stage = stage
            ranking.save()

            if stage == 2:
                messages.success(
                    request,
                    _("Thank you for submitting your rankings to the previous "
                      "set of questions."),
                )
            elif stage == 3:
                messages.success(
                    request,
                    _("Thank you for submitting your rankings to the "
                      "questions. On this final page of the survey, we would "
                      "like to understand more about you and your students."),
                )
            else:
                messages.success(
                    request,
                    _("Thank you for the answers."),
                )

            return redirect(
                reverse('rank_stage', args=[hash_id, stage + 1]),
            )

        else:
            messages.error(request,
                           _("Please rank all of the questions provided."),
                           extra_tags="danger")

    else:
        formset = RankingEntryFormset(queryset=entries_stage)

    page_header = _("Page {} of 4").format(ranking.stage + 1)

    context = {
        'title': _("Questions for Computing Education Researchers"),
        'hash_id': hash_id,
        'formset': formset,
        'page_header': page_header,
    }

    return render(request, "ranker/stage.html", context)
