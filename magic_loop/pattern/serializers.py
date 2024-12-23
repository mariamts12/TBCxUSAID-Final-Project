from rest_framework import serializers

from .models import PatternTag, Category, Pattern, Material, YarnType


class PatternTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = PatternTag
        fields = "__all__"


class MaterialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Material
        fields = ["pattern", "name", "amount", "unit"]


class DetailCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = [
            "id",
            "name",
            "description",
            "parent",
            "subcategories"
        ]


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = [
            "id",
            "name"
        ]


class AddCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = [
            "id",
            "name",
            "description",
            "parent"
        ]


class YarnTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = YarnType
        fields = ["name"]


class PatternDetailSerializer(serializers.ModelSerializer):
    tags = PatternTagSerializer(source="tag", many=True, read_only=True)
    categories = DetailCategorySerializer(source="category", many=True, read_only=True)
    materials = MaterialSerializer(many=True, read_only=True)
    yarn_types = YarnTypeSerializer(source="yarn_type", many=True, read_only=True)

    class Meta:
        model = Pattern
        fields = [
            "id",
            "author",
            "title",
            "description",
            "image",
            "file",
            "text_pattern",
            "difficulty",
            "yarn_types",
            "hook_or_needle_size",
            "saved_count",
            "created_at",
            "tags",
            "categories",
            "materials"
        ]


class PatternSerializer(serializers.ModelSerializer):
    tags = PatternTagSerializer(source="tag", many=True, read_only=True)
    categories = CategorySerializer(source="category", many=True, read_only=True)
    # yarn_types = YarnTypeSerializer(source="yarn_type", many=True, read_only=True)

    class Meta:
        model = Pattern
        fields = [
            "id",
            "author",
            "title",
            "image",
            "difficulty",
            "saved_count",
            "tags",
            "categories"
        ]


class AddPatternSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pattern
        fields = [
            "title",
            "description",
            "image",
            "file",
            "text_pattern",
            "difficulty",
            "yarn_type",
            "hook_or_needle_size",
            "category",
            "tag",
        ]

    def validate(self, data):
        if not data.get("file") and not data.get("text_pattern"):
            raise serializers.ValidationError("You must provide either a file or a text pattern.")

        if data.get("hook_or_needle_size") and data["hook_or_needle_size"] <= 0:
            raise serializers.ValidationError(
                {"hook_or_needle_size": "Crochet hook or Knitting needle size must be positive."}
            )

        return data
