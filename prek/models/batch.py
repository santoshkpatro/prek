from django.db import models
from .base import BaseUUIDModel
from .course import Course


class Batch(BaseUUIDModel):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    start_date = models.DateField(blank=True, null=True)

    class Meta:
        db_table = 'batches'

    def __str__(self) -> str:
        return self.name
