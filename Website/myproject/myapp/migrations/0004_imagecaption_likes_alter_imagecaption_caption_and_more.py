# Generated by Django 4.1.7 on 2023-04-30 00:50

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('myapp', '0003_alter_imagecaption_created_at'),
    ]

    operations = [
        migrations.AddField(
            model_name='imagecaption',
            name='likes',
            field=models.ManyToManyField(blank=True, related_name='liked_images', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='imagecaption',
            name='caption',
            field=models.CharField(max_length=200),
        ),
        migrations.DeleteModel(
            name='Like',
        ),
    ]
