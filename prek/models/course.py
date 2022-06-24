from django.db import models
from .user import User
from .base import BaseUUIDModel


class Course(BaseUUIDModel):
    instructor = models.ForeignKey(User, on_delete=models.PROTECT, related_name='instructor_courses')
    title = models.CharField(max_length=300)
    description = models.TextField(blank=True, null=True)
    thumbnail_url = models.CharField(max_length=200, blank=True, null=True)
    preview_url = models.CharField(max_length=200, blank=True, null=True)
    is_free = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True, db_index=True)

    class Meta:
        db_table = 'courses'

    def __str__(self) -> str:
        return self.title
