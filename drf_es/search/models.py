from django.db import models


class Stackoverflow(models.Model):
    questions = models.CharField(max_length=255)
    tags = models.TextField()
    link = models.IntegerField()
    views = models.IntegerField()
    answers = models.IntegerField()
    votes = models.IntegerField()

    def __str__(self):
        return self.questions




