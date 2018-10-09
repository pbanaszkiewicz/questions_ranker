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


class Category(CreatedUpdatedMixin, AuthoredMixin, models.Model):
    name = models.CharField(
        null=False, blank=False,
        max_length=255,
        verbose_name=_("Category name"),
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Category")
        verbose_name_plural = _("Categories")


class Question(ActiveMixin, CreatedUpdatedMixin, AuthoredMixin, models.Model):
    """A simple question model.

    "Some questions don't need answers" - somebody."""
    content = models.TextField(
        blank=False,
        verbose_name=_("Question content"),
    )

    category = models.ForeignKey(
        Category, on_delete=models.PROTECT,
        blank=False,
        verbose_name=_("Question category")
    )

    def __str__(self):
        title = self.content
        if len(self.content) > 50:
            title = "{}...".format(self.content[:50])

        return "Question #{}: {}".format(self.pk, title)


class Ranking(CreatedUpdatedMixin, models.Model):
    """A ranking, ie. list of questions with their rank, contributed by
    a user."""
    hash_id = models.CharField(
        null=False, blank=False, unique=True,
        max_length=255,
        verbose_name=_("Unique hash"),
    )
    stage = models.PositiveIntegerField(
        null=False, blank=False, default=0,
        verbose_name=_("Completion stage"),
        help_text=_("0 - not started, "
                    "1 - answered email, "
                    "2 - first set completed, "
                    "3 - second set completed, "
                    "4 - answered demographic")
    )
    category_stage1 = models.ForeignKey(
        Category, on_delete=models.PROTECT,
        null=True, blank=True, default=None,
        verbose_name=_("Stage 1 category (randomly chosen)"),
        related_name='ranking_stage1',
    )
    category_stage2 = models.ForeignKey(
        Category, on_delete=models.PROTECT,
        null=True, blank=True, default=None,
        verbose_name=_("Stage 2 category (randomly chosen)"),
        related_name='ranking_stage2',
    )
    entries = models.ManyToManyField(
        Question, through='RankingEntry',
    )

    TIME_SPENT_CHOICES = (
        ('none', _("None")),
        ('tens', _("Tens of hours")),
        ('hundreds', _("Hundreds of hours")),
        ('primary', _("Primary activity")),
    )
    teaching_children_in_schools = models.CharField(
        null=False, blank=False, default="", max_length=50,
        choices=TIME_SPENT_CHOICES,
        verbose_name=_("How much time you have spent in the last five years "
                       "teaching children in schools?"),
    )
    teaching_teens_in_schools = models.CharField(
        null=False, blank=False, default="", max_length=50,
        choices=TIME_SPENT_CHOICES,
        verbose_name=_("How much time you have spent in the last five years "
                       "teaching teens in schools?"),
    )
    teaching_students = models.CharField(
        null=False, blank=False, default="", max_length=50,
        choices=TIME_SPENT_CHOICES,
        verbose_name=_("How much time you have spent in the last five years "
                       "teaching college/university students?"),
    )
    teaching_adults = models.CharField(
        null=False, blank=False, default="", max_length=50,
        choices=TIME_SPENT_CHOICES,
        verbose_name=_("How much time you have spent in the last five years "
                       "teaching adults in workplaces (e.g. staff training)?"),
    )
    teaching_children_free_range = models.CharField(
        null=False, blank=False, default="", max_length=50,
        choices=TIME_SPENT_CHOICES,
        verbose_name=_("How much time you have spent in the last five years "
                       "teaching children in free-range programs (i.e. "
                       "outside traditional classrooms)?"),
    )
    teaching_teens_free_range = models.CharField(
        null=False, blank=False, default="", max_length=50,
        choices=TIME_SPENT_CHOICES,
        verbose_name=_("How much time you have spent in the last five years "
                       "teaching teens in free-range programs (i.e. "
                       "outside traditional classrooms)?"),
    )
    teaching_adults_free_range = models.CharField(
        null=False, blank=False, default="", max_length=50,
        choices=TIME_SPENT_CHOICES,
        verbose_name=_("How much time you have spent in the last five years "
                       "teaching adults in free-range programs (i.e. "
                       "outside traditional classrooms)?"),
    )

    DAILY_ACCESS_CHOICES = (
        ('none', _("None")),
        ('quarter', _("Less than a quarter")),
        ('quertertothree', _("One quarter to three quarters")),
        ('morethanthree', _("More than three quarters")),
    )
    daily_home_computer = models.CharField(
        null=False, blank=False, default="", max_length=50,
        choices=DAILY_ACCESS_CHOICES,
        verbose_name=_("What fraction of your learners has daily access to "
                       "laptop or computer at home?"),
    )
    daily_school_computer = models.CharField(
        null=False, blank=False, default="", max_length=50,
        choices=DAILY_ACCESS_CHOICES,
        verbose_name=_("What fraction of your learners has daily access to "
                       "school or library computer?"),
    )
    daily_smartphone = models.CharField(
        null=False, blank=False, default="", max_length=50,
        choices=DAILY_ACCESS_CHOICES,
        verbose_name=_("What fraction of your learners has daily access to "
                       "tablet or smartphone?"),
    )
    daily_broadband = models.CharField(
        null=False, blank=False, default="", max_length=50,
        choices=DAILY_ACCESS_CHOICES,
        verbose_name=_("What fraction of your learners has daily access to "
                       "high-speed / broadband internet?"),
    )
    daily_lowspeed = models.CharField(
        null=False, blank=False, default="", max_length=50,
        choices=DAILY_ACCESS_CHOICES,
        verbose_name=_("What fraction of your learners has daily access to "
                       "only low-speed internet?"),
    )

    PERSONAL_INVOLVEMENT_CHOICES = (
        ('none', _("I have no involvement.")),
        ('rare', _("I sometimes read results from studies or go to "
                   "presentations but don't do any research myself.")),
        ('regular', _("I regularly read results from studies or go to "
                      "presentations but don't do any research myself.")),
        ('occasional', _("I occasionally dabble in computing education "
                         "research myself.")),
        ('primary', _("Computing education research is my primary occuption.")),
    )
    comp_research_involvement = models.CharField(
        null=False, blank=False, default="", max_length=50,
        choices=PERSONAL_INVOLVEMENT_CHOICES,
        verbose_name=_("How involved you are personally in "
                       "computing education research?"),
        help_text=_("Select the option that best describes you."),
    )

    def __str__(self):
        return "Person ranking #{} ({}, compl. stage {})".format(
            self.pk, self.hash_id, self.stage,
        )

    class Meta:
        verbose_name = "Person ranking"
        verbose_name_plural = "Person rankings"


class RankingEntry(models.Model):
    """A representation of a question and its rank."""
    ranking = models.ForeignKey(
        Ranking, on_delete=models.CASCADE,
        null=False, blank=False,
        verbose_name=_("Ranking"),
    )
    question = models.ForeignKey(
        Question, on_delete=models.PROTECT,
        null=False, blank=False,
        verbose_name=_("Question"),
    )
    RANK_CHOICES = (
        ('essential', _("Essential")),
        ('worthwhile', _("Worthwhile")),
        ('unimportant', _("Unimportant")),
        ('unwise', _("Unwise")),
        ('dont_understand', _("I don't understand")),
    )
    rank = models.CharField(
        null=True, blank=False,
        max_length=255,
        choices=RANK_CHOICES,
        verbose_name=_("Selected rank"),
    )
    stage = models.PositiveIntegerField(
        null=False, blank=False,
        verbose_name=_("Trial stage"),
        help_text=_("Number of round of questions"),
    )

    class Meta:
        verbose_name = _("Ranking entry")
        verbose_name_plural = _("Ranking entries")


class DrawEntry(models.Model):
    email = models.EmailField(
        null=False, blank=True, default="",
        verbose_name="E-mail address",
        help_text="Provide if you want to enter the draw or to receive"
                  " paper(s) about this study."
    )
    BOOLEAN_CHOICES = (
        (True, _("Yes")),
        (False, _("No")),
    )
    draw = models.BooleanField(
        null=False, blank=False, default=False,
        choices=BOOLEAN_CHOICES,
        verbose_name="I want to take part in the draw",
    )
    paper = models.BooleanField(
        null=False, blank=False, default=False,
        choices=BOOLEAN_CHOICES,
        verbose_name="I want to receive the paper(s) about this study",
    )

    class Meta:
        verbose_name = _("Draw entry")
        verbose_name_plural = _("Draw entries")


class QuestionSummary(Question):
    class Meta:
        # with `proxy = True` there's no "physical" database table created
        proxy = True
        verbose_name = 'Question summary'
        verbose_name_plural = 'Questions summary'
