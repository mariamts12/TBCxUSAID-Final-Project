from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import PatternTagViewSet, PatternViewSet, CategoryViewSet, MaterialViewSet, YarnTypeViewSet

app_name = "patterns"

router = DefaultRouter()
router.register("pattern-tags", PatternTagViewSet, basename="pattern_tags")
router.register("yarn-types", YarnTypeViewSet, basename="yarn_types")
router.register("patterns", PatternViewSet, basename="patterns")
router.register("categories", CategoryViewSet, basename="categories")
router.register("materials", MaterialViewSet, basename="materials")

urlpatterns = [
    path("", include(router.urls), name="router"),
]
