import datetime

from django.db import models

from app.user.model import User


class Tag(models.Model):
    name = models.CharField(max_length=60)
    # notes = models.ForeignKey(Note, on_delete=models.CASCADE, related_name="tags")


class Note(models.Model):
    class Meta:
        ordering = ['-update_date']

    # using implicit id
    title = models.CharField(max_length=400)
    content = models.CharField(max_length=1000000)
    update_date = models.DateField(default=datetime.date.today)
    version = models.IntegerField(default=0)
    user = models.ForeignKey(User, on_delete=models.RESTRICT, related_name="notes")
    tags = models.ManyToManyField(Tag, related_name="notes")
