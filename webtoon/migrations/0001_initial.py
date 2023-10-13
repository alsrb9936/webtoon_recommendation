# Generated by Django 4.2.5 on 2023-10-02 06:12

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Webtoon',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('author', models.CharField(max_length=200)),
                ('rating', models.FloatField()),
                ('image', models.TextField()),
                ('webtoon_url', models.TextField()),
                ('genre', models.CharField(max_length=200)),
                ('week', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='User_Webtoon',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rating', models.FloatField()),
                ('review', models.TextField(null=True)),
                ('reviewer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('webtoon', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='webtoon.webtoon')),
            ],
        ),
        migrations.AddConstraint(
            model_name='user_webtoon',
            constraint=models.UniqueConstraint(fields=('webtoon', 'reviewer'), name='unique_review'),
        ),
    ]
