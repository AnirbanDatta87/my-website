# Generated by Django 2.2.6 on 2019-10-28 07:43

import ckeditor_uploader.fields
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('category', models.CharField(choices=[('General', 'General'), ('Python', 'Python'), ('Django', 'Django'), ('AI', 'AI'), ('ML', 'ML'), ('Analytics', 'Analytics'), ('DS', 'DS')], default='general', max_length=20)),
                ('tagline', models.TextField()),
                ('content', ckeditor_uploader.fields.RichTextUploadingField(blank=True, null=True)),
                ('thumbnail', models.ImageField(upload_to='')),
                ('date', models.DateTimeField(default=django.utils.timezone.now)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('-date',),
            },
        ),
    ]
