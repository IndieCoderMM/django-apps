from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _

class ToDoList(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='todolist', null=False)
    name = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Item(models.Model):
    class Priority(models.TextChoices):
        P1 = "!", _('WAITING')
        P2 = "!!", _('TODO')
        P3 = "!!!", _('URGENT')

    todolist = models.ForeignKey(ToDoList, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    priority = models.CharField(max_length=3, choices=Priority.choices, default=Priority.P1)
    created_at = models.DateTimeField(auto_now=True)
    description = models.CharField(max_length=200, null=True, blank=True)
    due_date = models.DateTimeField(null=True)
    complete = models.BooleanField(default="False")

    def __str__(self):
        return self.name


