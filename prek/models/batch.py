from django.db import models
from .base import BaseUUIDTimeStampedModel
from .course import Course


class Batch(BaseUUIDTimeStampedModel):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    start_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = 'batches'

    def __str__(self) -> str:
        return self.name
