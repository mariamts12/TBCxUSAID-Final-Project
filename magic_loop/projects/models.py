from django.db import models
from django.conf import settings
from pattern.models import Pattern, YarnType


class Project(models.Model):
    class StatusChoices(models.TextChoices):
        IN_PROGRESS = 'in_progress', 'In Progress'
        COMPLETED = 'completed', 'Completed'

    user = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='projects')
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    pattern = models.ForeignKey(Pattern, null=True, blank=True, on_delete=models.SET_NULL)
    yarn_type = models.ForeignKey(to=YarnType, on_delete=models.SET_NULL, null=True)
    hook_or_needle_size = models.CharField(max_length=50)
    status = models.CharField(max_length=20, choices=StatusChoices.choices, default=StatusChoices.IN_PROGRESS)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    time_spent = models.DurationField(null=True, blank=True)

    def __str__(self):
        return self.name


class ProjectImage(models.Model):
    project = models.ForeignKey(to=Project, on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(upload_to='project_photos/')

