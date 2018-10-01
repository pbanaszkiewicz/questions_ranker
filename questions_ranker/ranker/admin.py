from django.contrib import admin
from django.db.models import Sum, Count, Avg, Min, Max, StdDev, Q, F
from django.utils.translation import ugettext_lazy as _
from .models import (
    Category,
    Question,
    Ranking,
    QuestionSummary,
    RankingEntry,
)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    date_hierarchy = 'created_at'


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = [
        '__str__',
        'active',
        'category',
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

        assert RankingEntry.RANK_CHOICES[0][0] == 'essential'
        assert RankingEntry.RANK_CHOICES[1][0] == 'worthwhile'
        assert RankingEntry.RANK_CHOICES[2][0] == 'unimportant'
        assert RankingEntry.RANK_CHOICES[3][0] == 'unwise'
        assert RankingEntry.RANK_CHOICES[4][0] == 'dont_understand'

        metrics = {
            'essential_count': Count(
                'rankingentry__pk',
                filter=Q(rankingentry__rank='essential'),
            ),
            'worthwhile_count': Count(
                'rankingentry__pk',
                filter=Q(rankingentry__rank='worthwhile'),
            ),
            'unimportant_count': Count(
                'rankingentry__pk',
                filter=Q(rankingentry__rank='unimportant'),
            ),
            'unwise_count': Count(
                'rankingentry__pk',
                filter=Q(rankingentry__rank='unwise'),
            ),
            'dont_understand_count': Count(
                'rankingentry__pk',
                filter=Q(rankingentry__rank='dont_understand'),
            ),
            'total_ranks': Count(
                'rankingentry__pk',
                filter=Q(rankingentry__rank__isnull=False),
            ),
        }

        response.context_data['summary'] = (
            qs
            .annotate(**metrics)
            .order_by('category', 'pk')
        )

        response.context_data['title'] = _("Summary of questions")

        return response
