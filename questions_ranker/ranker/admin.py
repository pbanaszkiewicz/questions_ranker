from django.contrib import admin
from django.db.models import Sum, Count, Avg, Min, Max, StdDev, Q, F
from django.utils.translation import ugettext_lazy as _
from .models import (
    Question,
    Ranking,
    QuestionSummary,
)


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = [
        '__str__',
        'active',
        'author',
        'created_at',
        'last_updated_at',
    ]
    date_hierarchy = 'created_at'


class EntryInlineAdmin(admin.TabularInline):
    model = Ranking.entries.through
    extra = 5


@admin.register(Ranking)
class RankingAdmin(admin.ModelAdmin):
    date_hierarchy = 'created_at'
    # fields = [
    #     'author',
    #     'entries',
    # ]
    inlines = (EntryInlineAdmin, )


@admin.register(QuestionSummary)
class QuestionSummaryAdmin(admin.ModelAdmin):
    # date_hierarchy = 'created_at'
    change_list_template = 'admin/question_summary_change_list.html'

    def changelist_view(self, request, extra_context=None):
        response = super().changelist_view(
            request,
            extra_context=extra_context,
        )

        try:
            qs = response.context_data['cl'].queryset
        except (AttributeError, KeyError):
            return response

        metrics = {
            'avg_rank': Avg('rankingentry__rank'),
            'min_rank': Min('rankingentry__rank'),
            'max_rank': Max('rankingentry__rank'),
            'total_ranks': Count('rankingentry__pk'),
        }

        response.context_data['summary'] = (
            qs
            .annotate(**metrics)
            .order_by('-avg_rank')
        )

        response.context_data['title'] = _("Summary of questions")

        return response
