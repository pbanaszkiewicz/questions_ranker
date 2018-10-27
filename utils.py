import csv
from django.db import transaction
from ranker.models import Category, Question, Ranking
from questions_ranker.users.models import User


@transaction.atomic
def bulk_add_questions(filename, update=False):
    admin = User.objects.get(username="admin")
    with open(filename, 'r') as f:
        reader = csv.DictReader(f, delimiter=',', quotechar='"')
        results = []
        for row in reader:
            cat, _ = Category.objects.get_or_create(name=row['Category'],
                                                    defaults=dict(author=admin))
            if update:
                res = Question.objects.filter(id=int(row['ID'])).update(
                    category=cat,
                    content=row['Question'],
                    author=admin,
                )
            else:
                res = Question.objects.create(
                    id=int(row['ID']),
                    content=row['Question'],
                    category=cat,
                    author=admin,
                )
            results.append(res)
    return results


@transaction.atomic
def bulk_add_rankings(filename, update=False):
    with open(filename, 'r') as f:
        lines = f.readlines()
        Ranking.objects.bulk_create(
            [
                Ranking(hash_id=line.strip(), stage=0)
                for line in lines
                if line
            ]
        )
