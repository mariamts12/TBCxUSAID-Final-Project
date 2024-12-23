from django.conf import settings
from django.core.validators import MinValueValidator
from django.db import models

from .managers import CategoryManager


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    parent = models.ForeignKey(to="self", related_name="subcategories", on_delete=models.SET_NULL, blank=True,
                               null=True)
    objects = CategoryManager()

    def __str__(self):
        return self.name


class PatternTag(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name


class YarnType(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name


class Pattern(models.Model):
    class DifficultyChoices(models.TextChoices):
        BEGINNER = 'beginner', 'Beginner'
        INTERMEDIATE = 'intermediate', 'Intermediate'
        ADVANCED = 'advanced', 'Advanced'

    author = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True,
                               related_name="patterns")
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    tips = models.TextField(blank=True)
    image = models.ImageField(upload_to='patterns/images/', blank=True, null=True)
    file = models.FileField(upload_to='patterns/files/', blank=True, null=True)
    text_pattern = models.TextField(blank=True, null=True)
    difficulty = models.CharField(max_length=20, choices=DifficultyChoices.choices)
    yarn_type = models.ManyToManyField(to=YarnType, related_name="patterns", blank=True)
    hook_or_needle_size = models.DecimalField(max_digits=5, decimal_places=2, help_text="Enter size in millimeters.")
    category = models.ManyToManyField(to=Category, related_name='patterns', blank=True)
    tag = models.ManyToManyField(to=PatternTag)
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def saved_count(self) -> int:
        return self.saved.count()

    def __str__(self):
        return self.title


class Material(models.Model):
    class UnitChoices(models.TextChoices):
        GRAMS = 'grams', 'Grams'
        METERS = 'meters', 'Meters'
        YARDS = 'yards', 'Yards'
        PIECES = 'pieces', 'Pieces'
        PAIRS = 'pairs', 'Pairs'
        NONE = 'none', 'None'

    pattern = models.ForeignKey(to=Pattern, on_delete=models.CASCADE, related_name="materials")
    name = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True,
                                 validators=[MinValueValidator(0)])
    unit = models.CharField(max_length=20, choices=UnitChoices.choices, default=UnitChoices.NONE)

    def __str__(self):
        return self.name
