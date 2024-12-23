import django_filters
from django.db.models import Q

from .models import Project


class ProjectFilter(django_filters.FilterSet):
    search = django_filters.CharFilter(method="filter_search", label="Search")
    pattern_id = django_filters.NumberFilter(field_name="pattern__id", label="Pattern ID")
    user_id = django_filters.NumberFilter(field_name="user__id", label="User ID")
    yarn_type = django_filters.NumberFilter(field_name="yarn_type__id", label="Yarn Type")
    status = django_filters.ChoiceFilter(field_name="status", choices=Project.StatusChoices.choices,
                                         label="Status")
    time_spent = django_filters.NumberFilter(method="filter_time_spent", label="Time Spent")

    class Meta:
        model = Project
        fields = ["pattern_id", "user_id", "yarn_type", "status", "time_spent"]

    @staticmethod
    def filter_search(queryset, name, value):
        return queryset.filter(Q(name__icontains=value) | Q(description__icontains=value))

    @staticmethod
    def filter_time_spent(queryset, name, value):
        return queryset.filter(Q(time_spent__lte=value))
