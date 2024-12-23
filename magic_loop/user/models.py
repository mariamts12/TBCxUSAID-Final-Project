from django.contrib.auth.models import AbstractUser
from django.db import models

from pattern.models import Pattern


class User(AbstractUser):
    email = models.EmailField(unique=True)
    saved_patterns = models.ManyToManyField(to=Pattern, related_name="saved", blank=True)

    @property
    def patterns_count(self) -> int:
        return self.patterns.count()

    @property
    def saved_patterns_count(self):
        return self.saved_patterns.count()
