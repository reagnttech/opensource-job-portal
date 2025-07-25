# Generated by Django 5.2.2 on 2025-06-17 08:29

import peeldb.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("peeldb", "0060_certification"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="resume",
            field=models.FileField(
                blank=True,
                help_text="Upload your resume in PDF, DOC, DOCX, RTF, or ODT format (max 1MB)",
                max_length=2000,
                null=True,
                upload_to=peeldb.models.resume_upload_path,
            ),
        ),
    ]
