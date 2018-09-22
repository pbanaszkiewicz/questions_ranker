from django.db import models
from django.utils.translation import ugettext_lazy as _
from questions_ranker.users.models import User

#-----------------------------------------------------------------------------
#-----------------------------------------------------------------------------
#-----------------------------------------------------------------------------

class ActiveMixin(models.Model):
    """This mixin adds 'active' field for marking model instances as active or
    inactive (e.g. closed or in 'not have to worry about it' state)."""
    active = models.BooleanField(
        null=False, blank=True, default=True,
        verbose_name=_('Active'),
    )

    class Meta:
        abstract = True


class CreatedUpdatedMixin(models.Model):
    """This mixin provides two fields for storing instance creation time and
    last update time. It's faster than checking model revisions (and they
    aren't always enabled for some models)."""
    created_at = models.DateTimeField(
        null=False, blank=False,
        auto_now_add=True,
        verbose_name=_("Created at"),
        help_text=_("Creation timestamp"),
    )
    last_updated_at = models.DateTimeField(
        null=True, blank=True,
        auto_now=True,
        verbose_name=_("Last updated at"),
        help_text=_("Last update timestamp"),
    )

    class Meta:
        abstract = True


class AuthoredMixin(models.Model):
    """Mixin class for providing an author field."""
    author = models.ForeignKey(
        User, on_delete=models.PROTECT,
        null=False, blank=False,
        verbose_name=_("Author"),
    )

    class Meta:
        abstract = True

#-----------------------------------------------------------------------------
#-----------------------------------------------------------------------------
#-----------------------------------------------------------------------------

class Question(ActiveMixin, CreatedUpdatedMixin, AuthoredMixin, models.Model):
    """A simple question model.

    "Some questions don't need answers" - somebody."""
    content = models.CharField(
        null=False, blank=False,
        max_length=255,
        verbose_name=_("Question content"),
    )

    def __str__(self):
        title = self.content
        if len(self.content) > 50:
            title = "{}...".format(self.content[:50])

        return "Question #{}: {}".format(self.pk, title)


class Ranking(CreatedUpdatedMixin, AuthoredMixin, models.Model):
    """A ranking, ie. list of questions with their rank, contributed by
    a user."""
    entries = models.ManyToManyField(
        Question, through='RankingEntry',
    )

    def __str__(self):
        return "User <{}> ranking #{}".format(str(self.author), self.pk)


class RankingEntry(models.Model):
    """A representation of a question and its rank."""
    ranking = models.ForeignKey(
        Ranking, on_delete=models.CASCADE,
        null=False, blank=False,
        verbose_name=_("Ranking"),
    )
    question = models.ForeignKey(
        Question, on_delete=models.CASCADE,
        null=False, blank=False,
        verbose_name=_("Question"),
    )
    rank = models.PositiveIntegerField(
        null=False, blank=False,
        verbose_name=_("Selected rank"),
    )
    trial_round = models.PositiveIntegerField(
        null=False, blank=False,
        verbose_name=_("Trial round"),
        help_text=_("Number of round of questions"),
    )

    class Meta:
        verbose_name = "Ranking entry"
        verbose_name_plural = "Ranking entries"


class QuestionSummary(Question):
    class Meta:
        # with `proxy = True` there's no "physical" database table created
        proxy = True
        verbose_name = 'Question summary'
        verbose_name_plural = 'Questions summary'