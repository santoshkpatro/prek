from django.db import models
from .base import BaseUUIDTimeStampedModel
from .course import Course
from .batch import Batch


class Lesson(BaseUUIDTimeStampedModel):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='course_lessons')
    batch = models.ForeignKey(Batch, on_delete=models.CASCADE, related_name='batch_lessons')
    title = models.CharField(max_length=300)
    description = models.TextField(blank=True, null=True)
    video_url = models.CharField(max_length=200, blank=True, null=True)
    resource_url = models.CharField(max_length=200, blank=True, null=True)
    lesson_link = models.CharField(max_length=300, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    schedule_on = models.DateTimeField(blank=True, null=True)
    is_complete = models.BooleanField(default=False)

    class Meta:
        db_table = 'lessons'

    def __str__(self) -> str:
        return self.title
