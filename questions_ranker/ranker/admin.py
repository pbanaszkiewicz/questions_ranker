from django.contrib import admin
from django.db.models import Sum, Count, Avg, Min, Max, StdDev, Q, F
from django.utils.translation import ugettext_lazy as _
from .models import (
    Category,
    Question,
    Ranking,
    QuestionSummary,
    RankingEntry,
    DrawEntry,
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
    extra = 0
    can_delete = False
    readonly_fields = ['question', 'rank', 'stage']

    def has_add_permission(self, *args, **kwargs):
        return False

    def has_delete_permission(self, *args, **kwargs):
        return False

    def has_change_permission(self, *args, **kwargs):
        return False


@admin.register(Ranking)
class RankingAdmin(admin.ModelAdmin):
    date_hierarchy = 'created_at'
    readonly_fields = [
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
    ]
    inlines = [EntryInlineAdmin]


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

        # gather rank names from field's choices
        ranks = [i[0] for i in RankingEntry.RANK_CHOICES]
        # dict comprehension building annotation data
        # FIELD_count: Count with filter on `rankingentry__rank`
        metrics = {
            ('{}_count'.format(k)): Count(
                'rankingentry__pk',
                filter=Q(rankingentry__rank=k)
            )
            for k in ranks
        }
        metrics['total_ranks'] = Count(
            'rankingentry__pk',
            filter=Q(rankingentry__rank__isnull=False),
        )

        response.context_data['summary'] = (
            qs
            .select_related('category')
            .annotate(**metrics)
            .order_by('category', 'pk')
        )

        response.context_data['title'] = _("Summary of questions")

        return response


@admin.register(DrawEntry)
class DrawEntryAdmin(admin.ModelAdmin):
    readonly_fields = ['email', 'draw', 'paper']

    def has_add_permission(self, *args, **kwargs):
        return False

    def has_delete_permission(self, *args, **kwargs):
        return False

    def has_change_permission(self, *args, **kwargs):
        return False
