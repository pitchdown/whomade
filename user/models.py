from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    first_name = None
    last_name = None
    correct_answers = models.IntegerField(default=0)
    wrong_answers = models.IntegerField(default=0)
    total_questions = models.IntegerField(default=0)
    total_score = models.IntegerField(default=0)

    @property
    def average_guess(self):
        if self.total_questions > 0:
            return round(self.correct_answers / self.total_questions, 2)
        return 0