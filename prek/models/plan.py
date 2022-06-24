from django.db import models
from .base import BaseUUIDModel
from .course import Course


class Plan(BaseUUIDModel):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='course_plans')
    name = models.CharField(max_length=50)
    description = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    monthly_price = models.DecimalField(max_digits=8, decimal_places=2)
    monthly_discount = models.DecimalField(max_digits=8, decimal_places=2)
    yearly_price = models.DecimalField(max_digits=8, decimal_places=2)
    yearly_discount = models.DecimalField(max_digits=8, decimal_places=2)

    class Meta:
        db_table = 'plans'

    def __str__(self) -> str:
        return self.name
