# Generated by Django 5.1.3 on 2024-12-23 18:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("pattern", "0002_initial"),
        ("projects", "0002_remove_project_yarn_type_project_yarn_type"),
    ]

    operations = [
        migrations.AlterField(
            model_name="project",
            name="yarn_type",
            field=models.ManyToManyField(
                blank=True, related_name="projects", to="pattern.yarntype"
            ),
        ),
    ]