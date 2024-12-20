import django_filters
from django.db.models import Q

from .models import Post


class PostFilter(django_filters.FilterSet):
    search = django_filters.CharFilter(method="filter_search", label="Search")
    tag_id = django_filters.NumberFilter(field_name="tag__id", label="Tag ID")
    personal = django_filters.BooleanFilter(method="filter_personal", label="Personal posts")

    class Meta:
        model = Post
        fields = ["tag_id", "personal"]

    @staticmethod
    def filter_search(queryset, name, value):
        return queryset.filter(Q(title__icontains=value) | Q(content__icontains=value))

    def filter_personal(self, queryset, name, value):
        if value:
            return queryset.filter(author=self.request.user)
        return queryset
