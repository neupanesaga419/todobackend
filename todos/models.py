from django.db import models
from django.contrib.auth.models import User


STATUS = (
    ("Working on It", "Working on It"),
    ("Not Started", "Not Started"),
    ("Completed", "Completed"),
    ("Need Guidance", "Need Guidance"),
)


class Todo(models.Model):
    title = models.CharField(max_length=120)
    description = models.TextField()
    completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=50, choices=STATUS, default="Not Started")
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.title
