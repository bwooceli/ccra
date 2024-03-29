# Generated by Django 4.2.5 on 2024-01-13 17:34

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="RaceOrganization",
            fields=[
                (
                    "guid",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("created_timestamp", models.DateTimeField(auto_now_add=True)),
                ("updated_timestamp", models.DateTimeField(auto_now=True)),
                ("name", models.CharField(max_length=255)),
                ("description", models.TextField(blank=True, null=True)),
                ("website", models.URLField(blank=True, null=True)),
                ("email", models.EmailField(blank=True, max_length=254, null=True)),
                (
                    "parent_organization",
                    models.ForeignKey(
                        blank=True,
                        help_text="Parent organization for this organization",
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="child_organizations",
                        to="race_organization.raceorganization",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
    ]
