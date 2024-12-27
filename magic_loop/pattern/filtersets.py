import django_filters
from django.db.models import Q

from .models import Pattern, Category


class BasePatternFilter(django_filters.FilterSet):
    search = django_filters.CharFilter(method="filter_search", label="Search")
    tag_id = django_filters.NumberFilter(field_name="tag__id", label="Tag ID")
    category = django_filters.NumberFilter(
        method="filter_category", label="Category ID"
    )
    yarn_type = django_filters.NumberFilter(
        field_name="yarn_type__id", label="Yarn Type"
    )
    difficulty = django_filters.ChoiceFilter(
        field_name="difficulty",
        choices=Pattern.DifficultyChoices.choices,
        label="Difficulty",
    )
    popular = django_filters.OrderingFilter(fields=(("count_saved", "popular"),), label="Popular")

    class Meta:
        model = Pattern
        fields = ["tag_id", "category", "yarn_type", "difficulty", "popular"]

    @staticmethod
    def filter_search(queryset, name, value):
        return queryset.filter(
            Q(title__icontains=value) | Q(description__icontains=value)
        )

    @staticmethod
    def filter_category(queryset, name, value):
        return queryset.filter(
            Q(category__in=Category.objects.get_all_subcategories(value))
        )


class PatternFilter(BasePatternFilter):
    user_id = django_filters.NumberFilter(field_name="author__id", label="User ID")

    class Meta(BasePatternFilter.Meta):
        fields = BasePatternFilter.Meta.fields + ["user_id"]
