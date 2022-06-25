from django.db import models
from .base import BaseUUIDTimeStampedModel
from .user import User
from .plan import Plan
from .course import Course


class Subscription(BaseUUIDTimeStampedModel):
    STATUS_CHOICES = (
        (0, 'valid'),
        (1, 'pending'),
        (2, 'cancelled'),
        (3, 'review'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_subscriptions')
    plan = models.ForeignKey(Plan, on_delete=models.SET_NULL, null=True)
    course = models.ForeignKey(Course, on_delete=models.SET_NULL, null=True)
    subscription_code = models.CharField(max_length=100, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    valid_from = models.DateTimeField()
    valid_upto = models.DateTimeField()
    note = models.TextField(blank=True, null=True)
    status = models.IntegerField(default=0, choices=STATUS_CHOICES)

    class Meta:
        db_table = 'subscriptions'
        unique_together = ['user', 'plan']

    def __str__(self) -> str:
        return str(self.id)
