from django.db import models
from custom_auth.models import CustomUser


NOT_STARTED = "Not Started"
WORKING = "Working on It"
COMPLETED = "Completed"
NEED_GUIDANCE = "Need Guidance"

STATUS = (
    (WORKING, WORKING),
    (NOT_STARTED, NOT_STARTED),
    (COMPLETED, COMPLETED),
    (NEED_GUIDANCE, NEED_GUIDANCE),
)


class Todo(models.Model):
    title = models.CharField(max_length=120)
    description = models.TextField()
    completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=50, choices=STATUS, default=NOT_STARTED)
    created_by = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.title
