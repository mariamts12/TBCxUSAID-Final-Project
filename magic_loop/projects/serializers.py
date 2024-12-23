from datetime import date

from rest_framework import serializers

from pattern.serializers import YarnTypeSerializer
from .models import Project, ProjectImage


class ProjectImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectImage
        fields = "__all__"


class ProjectDetailSerializer(serializers.ModelSerializer):
    yarn_types = YarnTypeSerializer(source="yarn_type", many=True, read_only=True)
    images = ProjectImageSerializer(many=True, read_only=True)

    class Meta:
        model = Project
        fields = [
            "id",
            "user",
            "name",
            "description",
            "pattern",
            "yarn_types",
            "hook_or_needle_size",
            "status",
            "start_date",
            "end_date",
            "time_spent",
            "images"
        ]


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = [
            "id",
            "user",
            "name",
            "pattern",
            "time_spent"
        ]


class CreateProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = [
            "name",
            "description",
            "pattern",
            "yarn_type",
            "hook_or_needle_size"
        ]


class UpdateProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = [
            "name",
            "description",
            "pattern",
            "yarn_type",
            "hook_or_needle_size",
            "status",
            "end_date",
            "time_spent"
        ]
        extra_kwargs = {
            'name': {'required': False},
        }

    def validate(self, data):
        if data.get('status') == 'completed' and not data.get('end_date'):
            data["end_date"] = date.today()
        return data


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectImage
        fields = ["image"]
