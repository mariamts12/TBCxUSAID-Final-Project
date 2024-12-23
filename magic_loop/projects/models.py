from django.db import models
from django.conf import settings
from pattern.models import Pattern, YarnType


class Project(models.Model):
    class StatusChoices(models.TextChoices):
        IN_PROGRESS = "in_progress", "In Progress"
        COMPLETED = "completed", "Completed"

    user = models.ForeignKey(
        to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="projects"
    )
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    pattern = models.ForeignKey(
        Pattern, null=True, blank=True, on_delete=models.SET_NULL
    )
    yarn_type = models.ManyToManyField(to=YarnType, related_name="projects", blank=True)
    hook_or_needle_size = models.CharField(max_length=50, null=True, blank=True)
    status = models.CharField(
        max_length=20, choices=StatusChoices.choices, default=StatusChoices.IN_PROGRESS
    )
    start_date = models.DateField(auto_now_add=True)
    end_date = models.DateField(null=True, blank=True)
    time_spent = models.DecimalField(
        null=True,
        blank=True,
        decimal_places=1,
        max_digits=5,
        help_text="Hours spent on project",
    )

    def __str__(self):
        return self.name


class ProjectImage(models.Model):
    project = models.ForeignKey(
        to=Project, on_delete=models.CASCADE, related_name="images"
    )
    image = models.ImageField(upload_to="project_photos/")
